#!/usr/bin/env python

# generate Makefiles to compile single source C and assembly files
# for rv64i architecture using the `musl`, `clang`, `compiler_rt` toolchain

import getopt, sys, pathlib, subprocess

def usage(script_name, err=None):
    if type(err) == list:
        for msg in err:
            print(msg)
    elif err:
        print(err)
    print(f'''\
    Generate template makefile and build a rv64i binary from c or asm source.
    The template is supposed to be of the format of Makefile.template

    {script_name} <options>

    Optional arguments
    --flags=<args>   specify additional compiler flags as a comma separated string
    -t <arg>         specify the path to the Makefile to be used as template
    -b <arg>         specify name of the target binary. default is value of argument -d
    -s <arg>         specify the source file to compile. default is value of argument -d
    -x <arg>         specify the type of source file. the supported ones are C or assembly source files
    --build          run make to build the target binary in the destination directory

    Non optional arguments
    -d <arg>        specify path to the directory of the build \
    ''')

def main():
    # parse command line arguments
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'hd:t:b:s:x:', ['flags=', 'help', 'build'])
    except getopt.GetoptError as err:
        usage(sys.argv[0], err)
        exit(2)
    
    # default Makefile to use as template
    template_file = \
        pathlib.Path(pathlib.Path.home() / 'dev/riscv/projects/Makefile.template') \
            .resolve()

    dest_dir = None
    ext = 'c'
    source_file = None
    target_binary = None
    compiler_flags = None
    build_target = False

    # filter out arguments and assign them to the right variables.
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(sys.argv[0])
            exit(2)
        if opt == '--flags':
            compiler_flags = arg.split(',')
        elif opt == '-d':
            dest_dir = pathlib.Path(arg).resolve()
        elif opt == '-s':
            source_file = pathlib.Path(arg).resolve()
        elif opt == '-x':
            ext = arg
        elif opt == '-t':
            template_file = pathlib.Path(arg).resolve()
        elif opt == '-b':
            target_binary = arg
        elif opt == '--build':
            build_target = True
        else:
            usage(sys.argv[0], f'invalid option: {opt} {arg}')
    
    # accumulate error messages and send them to user.
    err_messages = []

    # destination directory should be a directory
    if not dest_dir:
        err_messages.append('specify directory to put Makefile with option -d')
    elif dest_dir.is_file():
        err_messages.append('-d: destination for Makefile should be a directory')
    
    # print error messages and the usage of this tool.
    if err_messages:
        usage(sys.argv[0], err_messages)
        sys.exit(2)

    # filepath of the destination Makefile.
    dest_makefile = pathlib.Path(dest_dir / 'Makefile').resolve()

    # make source file the destination with the source file extension appended
    # to it.
    if not source_file:
        source_file = dest_dir / f'{dest_dir.parts[-1]}.{ext}'

    # source file should be relative to the destination directory. this is done
    # by checking if source_file  exists, is a file and is relative to the build directory
    if not (source_file.exists() and source_file.is_file() and source_file.parts[-1] in \
        [s.parts[-1] for s in dest_dir.glob('*')]):
            usage(sys.argv[0], f'there is no source file {source_file.parts[-1]} in destination')
            exit(2)

    if not target_binary:
        # target binary will be source file name without the extension
        target_binary = source_file.parts[-1][:source_file.parts[-1].index('.')]

    cflags = []
    body   = []

    # parse template makefile to make a new Makefile.
    with template_file.open() as tmp:
        for line in tmp.readlines():
            if line.startswith('#'):
                continue
            elif line.startswith('CFLAGS'):
                # put the flags in the cflag list
                cflags.append(line[line.index('=')+1 : len(line)].strip())
            else:
                body.append(line)

    # generate Makefile from the options.
    parsed_flags = parse_cflags(cflags, compiler_flags)
    parsed_body = parse_makefile_body(body, target_binary, source_file.parts[-1])

    # write the generated Makefile to into Makefile in source directory
    with dest_makefile.open('w') as mk:
        mk.write(parsed_flags)
        mk.write(parsed_body)

    if build_target:
        subprocess.check_call(['make'], shell=True, cwd=str(dest_dir))
    return

# add optional compiler flags to flags to be used
# in the generated Makefile
def parse_cflags(cflags, opt_flags=None):
    if opt_flags:
        for flag in opt_flags:
            if not (flag in cflags):
                cflags.append(flag)
    return f"CFLAGS = {' '.join(cflags).strip()}\n"

# parse the rest of the Makefile that does compilation and linking.
def parse_makefile_body(body, target_binary, source_filename):
    objfile = source_filename[:source_filename.index('.')] + '.o'
    for idx, line in enumerate(body):
        if len(line) < 6:
            continue
        if 'template.c' in line:
            line = line.replace('template.c', source_filename)
        if 'template.o' in line:
            line = line.replace('template.o', objfile)
        if 'template' in line:
            line = line.replace('template', target_binary)
        body[idx] = line
    return ''.join(body)
 
if __name__ == '__main__':
    main()
