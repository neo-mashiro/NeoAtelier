

# DevOps



## Building & Testing

- [Professional CMake](https://crascit.com/professional-cmake/)
- [Google Test](https://github.com/google/googletest)


## Releasing




## CI/CD

Some people are under the impression that GCC is the same as gcc which is the GNU C compiler, but it’s not true. Initially, GCC was only the GNU C Compiler, but nowadays, GCC (GNU Compiler Collections) provides many compilers, including gcc and g++. GCC refers to a collection of compilers, while gcc is only the C compiler. gcc and g++ are both compiler-drivers of the GCC, g++ is used to compile C++ programs. When we talk about GCC compiler/linker flags, they apply to both gcc and g++.

The g++ command is for both compiling and linking, depending on what the command line options are. Bonus: LLVM is a collection of compiler and toolchain technologies, while Clang is a compiler front-end for the C, C++, Objective-C, and Objective-C++ programming languages, built using LLVM as its back-end.

On Linux, what is `rpath` and `LD_LIBRARY_PATH` ? What about LD?

- `rpath` designates the run-time search path hard-coded in an executable file or library. Dynamic linking loaders use the `rpath` to find required libraries. When an executable is run, the dynamic linker/loader searches for its required shared libraries in a number of directories, including the standard system directories and any directories specified in the `LD_LIBRARY_PATH` environment variable. The `rpath` option allows developers to specify additional directories to search for shared libraries at runtime, without having to rely on environment variables. You can set it using the `-Wl,-rpath=<dir>` flag at link time.
- Note that on the command line, option `-rpath` is not the same as `-L`, `-L` tells ld where to look for libraries to link against when linking, whereas `-rpath` stores that path inside the executable or library so that the runtime dynamic linker can find the libraries. For example, `gcc -o app app.c -L/usr/local/lib -Wl,-rpath=/tmp/lib` adds `/tmp/lib` to the `app` executable as a run-time search path, this is mostly used when your libraries are outside the system library search path. Most of the time when you need `-Wl,-rpath=/some/weird/path`, you probably need `-L/some/weird/path` as well.
- `LD_LIBRARY_PATH` is a predefined environment variable in Linux/Unix that specifies a colon-separated list of directories where the dynamic linker should look for shared libraries when running a program. What’s special about it is that, the linker gives priority to paths in `LD_LIBRARY_PATH` over the standard library paths `/lib` and `/usr/lib`. The standard paths will still be searched, but only after the list of paths in `LD_LIBRARY_PATH` has been exhausted. `LD_LIBRARY_PATH` is Linux specific, on Windows you need to play with the `PATH` environment variable instead. To use `LD_LIBRARY_PATH`, set it on the command line or in the script before executing the program: `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/your/custom/path/`. While you can add some weird paths to `LD_LIBRARY_PATH` in the script, the `rpath` option can be better and more convenient for this.
- Both `rpath` and `LD_LIBRARY_PATH` are Linux only, they do not exist on Windows. `LD_LIBRARY_PATH` is colon separated, but `rpath` is semicolon-delimited.
- Bonus - `LD_LIBRARY_PATH` stands for “LOAD LIBRARY PATH” or sometimes called “LOADER LIBRARY PATH”.
- A word of caution - You should probably stay away from altering your `LD_LIBRARY_PATH`, if you do, make sure to restore it when you're done, or you might screw the build processes of other software in the system. If you are using rez, this won’t be a problem, because every rez-resolved environment is an independent folder in `/tmp`, if you are not using rez, pay attention before doing it.
- On Unix-like operating systems, LD is the linker, you can think of it as the loader if that’s easier to remember. It combines many compiled object and archive files, relocates their data, and ties up symbol references. Usually, the last step in compiling a program is to run `ld` command.
- There’s a very similar command called `ldd`, which is used to print the shared library dependencies of an executable or a shared library. `ldd` shows you the list of shared libraries that the executable requires to run, along with the full path of the shared library file. It's a useful tool for troubleshooting issues related to shared library dependencies, such as missing libraries or version mismatches. You can try `ldd /bin/ls` to see where the standard libraries are on your system (mostly in `/lib64`).

You should also know what is a soname and how it differs from the real name of a library, but that’s more complicated to discuss here.

---

It’s good to know the common compile/linker options (flags) for GCC because they mostly have the same names being used in CMake. For example, if you know what `-Wl,-rpath=<dir>` does, you must also know the Linux specific `rpath`, then it’s very much trivial to understand the CMake variable `CMAKE_INSTALL_RPATH` and what this CMake command does:

```cmake
set_target_properties(mytarget
    PROPERTIES
    INSTALL_RPATH "@loader_path/../lib;@loader_path/../thirdparty/lib"
)
```

- `-std=c++11` - Specify the C++ version or ISO standard version.
- `-l[mylib]` - Link to shared library or shared object. For example, `-lm` compiles against the shared library `libm` (basic math library, mostly C only). `-lpthread` compiles against the POSIX threads shared library. `-ld3d9` compiles against DirectX `d3d9.dll` and `-ld3d12` compiles against DirectX 12 `d3d12.dll`. Note that DirectX is for Windows exclusively so there’s not a `libd3d9.so` on Linux. We also have `-lvulkan`, `-lGL`, `-lglfw` for linking to Vulkan, OpenGL and GLFW, and there’s the very popular `-lboost_system` and `-lboost_filesystem`.
- Note that there’s no white space after `-l`, the flag name must immediately follow, the same rule applies to `-L`, `-I` and `-D` as well. For example, `g++ -L/path/to/lib -I/path/to/include -lmylib foo.cpp -o myapp`.
- `-L[/path/to/shared-libraries]` - Add search path to shared libraries, that is, a folder that contains `*.so`, `*.dll` or `*.dlyb` files, etc.
- `-I[/path/to/header-files]` - Add search path to header files `.h` or `.hpp`. Usually we have many include paths, so you can pass as many `-I` as you need.
- `-D[FLAG]` or `-D[FLAG]=VALUE` - Pass preprocessor flags to the header and source files so that `#ifdef FLAG` and `#if FLAG` evaluates to true. For example, `-DDEBUG` is equivalent to adding `#define DEBUG` to your code, `-DFOO=1` is equivalent to adding `#define FOO = 1`, and `-DVERSION="2.0.0"` is equivalent to adding `#define VERSION "2.0.0"`.
- `-c [foo.cpp]` - Compile source file into object code (input to linker). `-c` means compile only, don't run the linker.
- `-g` - Enable this flag will tell the compiler to generate debugging info so that you can view stacktraces in your code with GDB and Valgrind.
- `-g3` - Similar to `-g` but will generate even more debugging info for more detailed views, at the cost of making your code much larger.
- `-shared` - Build a shared library (`.so` on Unix-like OS, `.dylib` on MacOSX, or `.dll` on Windows).
- `-o [/path/to/output-file]` - Specify the name and path of the output file, of course.
- `-Wall` - Turn on all standard compiler warning flags, specifically `-Waddress, -Wcomment, -Wformat, -Wbool-compare, -Wuninitialized, -Wunknown-pragmas, -Wunused-value, -Wunused-value`, etc.
- `-Werror` - Turn any warning into a compilation error.
- `-Wextra` - Enable extra warning flags not enabled by `-Wall`, such as `-Wsign-compare` (C only), `-Wtype-limits`, `-Wuninitialized`.
- `-Wpendantic` - Issue all warning required by ISO C and ISO C++ standard, it issues warning whenever there are compiler extensions non-compliant to ISO C or C++ standard.
- `-Wunnused`, `-Wshadow`, `-Wpointer-arith`, `-Wconversion`, …, you can basically know what they are from their names. For example, `-Wshadow` warns you when a variable declaration hides a previous declaration in outer scope.
- `-W[name]` - Enable a specific warning flag, as we can see above.
- `-Wno-[name]` - Disable a specific warning flag, note that there’s a hyphen `-` after `-Wno`. For example, the opposite of `-Wunused` is `-Wno-unused`, and we also have `-Wno-pragmas`, `-Wno-invalid-memory-model`, etc.
- `-Wl,-verbose` - Enable verbose mode in the linking process. You may find this syntax weird at first, but it does make sense. Compared to `-W[name]` which sets the compiler warning flag, `-Wl,-[name]` sets the linker warning flag, the `l` in `-Wl` means the linker.
- `-Wl,-rpath=<dir>` - Set the Unix rpath. Note that `rpath` is semicolon-delimited so for multiple paths you would use `-Wl,rpath=/path/to/dir1;/path/to/dir2`, do not separate the paths by colons.
- `-Wl,-rpath=$ORIGIN` - Set the Unix `rpath` to the executable current directory.
- `-Wl,-dynamic-linker,/path/to/linker/ld-linux.so.2.1` - Change the default dynamic linker.
- `-static-libgcc`, `-static-libstdc++` - Statically link against the `libgcc` and `libstdc++` runtime library.
- `-O0` - Disable all optimization, faster compilation time, better for debugging builds. This allows you to step through code in the debugger.
- `-Og` - Only enable optimizations which do not affect debugging, but in practice it’s not always guaranteed, so better use `-O0`.
- `-O2`, `-O3` - Higher level of optimization. Slower compile-time, better for production builds. `-OFast` enables even more higher level of optimization than `-O3`.
- `-Os` - Optimize for size at the cost of speed, barely used unless your target is really large or your target runs on embedded systems.
- `-m32`, `-m64` - Generate code for a 32-bit or 64-bit environment. The 32-bit environment sets `int`, `long` and pointer to 32 bits and generates code that runs on any i386 system. The 64-bit environment sets `int` to 32 bits and `long` and pointer to 64 bits and generates code for AMD's x86-64 architecture.
- `-fno-exceptions` - Disable C++ exceptions (it may be better for embedded systems or anything where exceptiions may not be acceptable).
- `-fno-rtti` - Disable RTTI (Runtime Type Information). There are many texts around where game and embedded systems developers report that they disable RTTI due to performance concerns.

---

Conventionally, people use names `CFLAGS/CXXFLAGS` and `LDFLAGS` for compiler and linker flags respectively that are used during the compilation and linking processes of a software project. `CFLAGS/CXXFLAGS` controls the behavior of the compiler during compilation, while `LDFLAGS` controls the behavior of the linker during linking. Note that `CXX` just stands for C++ but can be used as a valid variable name, `CPP` is not used in that sense as it mostly refers to the file extension.

- `CFLAGS` or `CXXFLAGS` is a variable that contains options to be passed to the compiler (usually gcc or clang) when compiling the source code. These options may include optimization flags, warning flags, include paths, and macro definitions, among others. For example, `-O2` is an optimization flag that tells the compiler to optimize the code for speed, and `-I<path>` is an include path flag that tells the compiler where to look for header files.
- `LDFLAGS`, on the other hand, is a variable that contains options to be passed to the linker (usually ld or gold) when linking the compiled object files into an executable or shared library. These options may include library paths, library names, and linker flags, among others. For example, `-L<path>` is a library path flag that tells the linker where to look for libraries, and `-l<name>` is a library name flag that tells the linker which libraries to link against.

---

Object files are `*.obj` on Windows but `*.o` on Linux, Unix and MacOSX. An object file does not 1:1 map to a `.cpp` file or a translation unit, that’s a common misunderstanding! In fact, you can create an `.o` file for a single or for many source files. It is true that we usually compile every single source file into a single object file, but that’s just for the sake of speed so that we can take advantage of incremental builds.

Static libraries are `*.a` on Linux and `*.lib` on Windows, a static library is created by putting together several `.o` files, that’s exactly what the linker does.

Shared libraries and dynamic libraries are synonyms, they are the same thing. They are shared by many executables and they are dynamically loaded at runtime. Shared libraries are `*.so` (shared object) on Linux, `*.dylib` (dynamic library) on MacOSX, and `*.dll` (dynamically linked libraries) on Windows.

The diff between static and dynamic libraries? That’s too basic and you already know that, but does loading a shared library slow down your program at runtime with extra cost? NO. Shared libraries are only loaded once in physical memory by the OS, but its symbols' offset are virtually mapped to the memory table for each process, so each process will see the same library symbols in different addresses. When you run your program, the shared library you need is probably already loaded by the OS.

Object libraries are less known to most people, this is an advanced concept. Object libraries are code compiled into .o object files but not combined into a single library, they are almost like static libraries, except that they are only used in certain special cases. Most commonly, people want to improve performance by only building certain code files once that are needed for multiple targets, and that’s when object libraries can be useful. The core idea of creating object libraries is exactly the same as using precompiled headers pch.h for faster iteration, with the exception that it is targeting the program performance at runtime rather than the efficiency of build time.

---

Some people (like me) have been under the impression that CMake is a piece of shit software. That’s probably true for older versions of CMake (<=2.8) before C+11 even exists, but as it evolves over time, modern CMake (3.4+, or better 3.26+) has become super clean, powerful and elegant, and it’s been established as the industry standard for building C++ projects, that’s why Rez also uses CMake for building Python projects. CMake 3.11+ are said to be significantly faster than previous versions. CMake is more than just a build system, making good use of it can help you enforce a good modular design of your project.

In addition to a build system, over the years CMake has evolved into a family of development tools: CMake, CTest, CPack, and CDash. CMake is the build tool responsible for building software. CTest is a test driver tool, used to run regression tests. CPack is a packaging tool used to create platform-specific installers for software built with CMake. CDash is a web application for displaying testing results and performing continuous integration testing.

CMake is not a build system, it is a build system generator. On Linux, running CMake consists of 2 steps internally, a “Configure” step that processes your CMakeLists.txt file in memory, and a "Generate" step that actually creates the build files. The name “CMake” stems from the idea of creating a better cross-platform “make” system, where the letter “C” stands for “cross-platform”. On Linux, you can imagine that CMake is a layer/tool on top of make, and make is a layer/tool on top of the g++ command (assume we are using the GCC compiler instead of Clang/LLVM or MSVC).

A minimum “Hello, world!” example of CMake:

```cmake
cmake_minimum_required(VERSION 3.14)
project(MyApp)
set(CMAKE_CXX_STANDARD 14)
add_executable(myapp main.cpp)
install(TARGETS myapp DESTINATION /foo/bar/bin)
```

and this is how we can run `cmake` (when using `rez build ...` rez does everything for us behind the scenes).

```cmake
cd /root/to/your/project          # where the top-level CMakeLists.txt file is located
mkdir build && cd build
cmake ..                          # parse the top-level CMakeLists.txt and generate the build files
cmake --build .                   # invoke the build files to build your targets (compiling + linking)
cmake --build . --target install  # install your project (files, built targets, etc)
```

Note that if using relative paths in `install(...)`, the paths are relative to `${CMAKE_INSTALL_PREFIX}` which typically defaults to `/usr/local`, it won’t be installed to your project directory (otherwise other users cannot find it).

In CMake, every variable is a string. When a variable is undefined, it defaults to an empty string. To read a variable, use `${}`, this is called a __variable reference__. You can nest variable references: `${outer_${inner_var}_var}`. They will be evaluated from the inside out.

To define a variable on the command line, use `DFOO=Bar`. For example, suppose you are in the build folder and you run `cmake -DNAME=cat ..` to execute the `CMakeLists.txt` file in the parent folder, this will create a variable called `NAME` in `CMakeLists.txt` and its value `${NAME}` is equal to `"cat"`.

- To define a variable inside a CMake script, use the `set` command. For example, `set(THING "funk")` creates a variable called `THING` and sets its value `${THING}` to `"funk"`. Note that quotes around arguments are optional, as long as there are no spaces or variable references in the argument.

By convention, variable names are all CAPS, some people like to use lowercase for local variables though.

CMake does not have classes, but you can simulate a data structure by defining a group of variables with names that begin with the same prefix. When you see a list of variables starting with the same prefix, you can assume that they belong to the same group. That’s just a convention.

```cmake
set(PACKAGE OCIO)
set(${PACKAGE}_NAME "OpenColorIO")
set(${PACKAGE}_VERSION "2.0.1")
message("The version of ${PACKAGE}_NAME is ${PACKAGE}_VERSION")
```

In CMake, every statement is a command that takes a list of __string arguments__ and has __no return value__. Arguments are separated by (unquoted) spaces. For example, CMake has a math command that performs arithmetic. The first argument must be `EXPR`, the second argument is the name of the variable to assign, and the third argument is the expression to evaluate – all strings.

```cmake
math(EXPR MY_SUM "1 + 1")
math(EXPR DOUBLE_SUM "${MY_SUM} * 2")  # ${DOUBLE_SUM} will be 4
```

https://cmake.org/cmake/help/latest/manual/cmake-commands.7.html - A full list of all CMake native commands. For example, the `string` command lets you perform advanced string manipulation, including regular expression replacement. The `file` command can read or write files, or manipulate filesystem paths.

Even flow control statements are commands: the `if/endif` commands, `while/endwhile` commands, `foreach/endforeach` commands, etc.

White space doesn’t matter so there’s no indentation in CMake, but it’s common to indent the enclosed commands for readablity:

```cmake
if(WIN32)  # checks whether CMake's built-in variable WIN32 is set
    message("You're running CMake on Windows.")
elseif(APPLE)
    message("You're running CMake on MacOS.")
else()
    message("You're running CMake on other platforms.")
endif()
```

```cmake
set(x "1")
while(x LESS "100")
    message("${x}")
    math(EXPR x "${x} + 1")
endwhile()
```

https://cmake.org/cmake/help/latest/command/if.html and https://cmake.org/cmake/help/latest/command/foreach.html - See documentation for how to write a condition.

Since every variable is a string in CMake, there’s a rule for checking whether a condition `if(<constant>)` is true or false.

- True if the constant is `1`, `ON`, `YES`, `TRUE`, `Y`, or a non-zero number (including floating point numbers).
- False if the constant is `0`, `OFF`, `NO`, `FALSE`, `N`, `IGNORE`, `NOTFOUND`, the empty string, or ends in the suffix `-NOTFOUND`.
- Note that these named boolean constants are case-insensitive, so `YES/yes/Yes` all evaluate to true.
- Note that environment variables cannot be tested this way: `if(ENV{some_var})` will always evaluate to false.

`if` and `while` are different from other CMake commands in that if the name of a variable is specified without quotes, the command will use the variable’s value. So `while(x LESS "100")` is equivalent to `while("${x}" LESS "100")`, `if(x)` is equivalent to `if(${x})`, but for other commands we need to be explicit by using `${x}`.

---

In CMake, lists are just semicolon-delimited strings. When you pass a list variable to a macro or command, CMake will split the value at the semicolons and pass __multiple arguments__ to the enclosing command. For example:

```cmake
set(ARGS "EXPR;T;1 + 1")
math(${ARGS})  # equivalent to calling math(EXPR T "1 + 1")
```

If more than two arguments are passed to the set command, they are joined by semicolons, then assigned to the specified variable.

```cmake
set(MY_LIST These are separate arguments)      # this is how we create a list variable
set(MY_STRING "These are separate arguments")  # will be treated as a single string if quoted
message("${MY_LIST}")                          # These;are;separate;arguments
```

You can manipulate a list using the `list` command:

```cmake
list(REMOVE_ITEM MY_LIST "separate")
message("${MY_LIST}")  # These;are;arguments
```

The `foreach/endforeach` command accepts multiple arguments. It iterates over all arguments except the first, assigning each one to the named variable:

```cmake
foreach(ARG These are separate arguments)
    message("${ARG}")  # prints each word on a separate line
endforeach()
```

This is how we iterate over a list (CMake will split the variable’s value and pass multiple arguments to the command):

```cmake
foreach(ARG ${MY_LIST})  # CMake will split the variable's value and pass multiple arguments to the command
    message("${ARG}")    # again, prints each item on a separate line
endforeach()
```

There is also a more modern CMake foreach syntax.

```cmake
foreach(var IN ITEMS foo bar baz)
    message(${var})
endforeach()

foreach(var IN LISTS my_list)
    message(${var})
endforeach()

foreach(var IN LISTS my_list ITEMS foo bar baz)
    message(${var})
endforeach()
```

CMake script files with the extension `.cmake` are called CMake modules, they are CMake’s vehicle for enabling code reuse. Inside CMake modules, there are collections of functions and macros that are either CMake-defined or user-defined. In CMake macros and functions are universally referred to as commands, and they are the primary method of defining code that can be called multiple times.

```cmake
macro(macro_name arg1 arg2 ...)
    # body of the macro
endmacro()
```

This is how you can define a macro in CMake. Note that CMake allows different ways of ending a macro, depending on the preference of the developer.

- `endmacro()`: This is the simplest and most commonly used way to end a macro. It does not require any arguments.
- `endmacro(macro_name)`: This specifies the name of the macro that is being ended. It is useful when you have multiple macros in your CMake file and you want to make it clear which macro is being closed.
- `endmacro(macro_name arg1 arg2 ...)`: This is similar to the previous example, but it includes the arguments of the macro. This can be useful when you have macros with many arguments and you want to make sure you are closing the correct one.

Macros can also have optional arguments, variable arguments, and use the `return()` command to return a value.

Optional arguments can be specified by providing default values for the macro arguments, for example:

```cmake
macro(macro_name arg1 arg2 arg3="default_value")
  # body of the macro
endmacro()
```

Variable arguments can be specified using the ... syntax, for example:

```cmake
macro(macro_name arg1 arg2 ...)
  # body of the macro
endmacro()
```

... indicates that the macro can accept an arbitrary number of additional arguments. The variable arguments can be accessed using the `ARGN` CMake variable, which contains a list of all the additional arguments passed to the macro. Note that `${ARGN}` contains all of the arguments passed to a macro after the named arguments, but `${ARGV}` is the full list of arguments passed to the function, including both named and unnamed (variable) arguments.

Macros run in the same scope as their caller. Therefore, all variables defined inside a macro are set in the caller's scope. This can sometimes lead to naming conflicts with variables defined outside of the macro. When defining macros, the best practice is to make sure the variable names do not conflict with any other variables in the caller’s scope, otherwise it can lead to subtle bugs or unexpected results like this:

```cmake
macro(print_list my_list)
    foreach(var IN LISTS my_list)
        message("${var}")
    endforeach()
endmacro()

set(my_list a b c d)
set(my_list_of_numbers 1 2 3 4)
print_list(my_list_of_numbers)
```

This code block will print `a b c d` (each on a separate line) instead of `1 2 3 4`, because the macro always takes in the variable `my_list` in the parent scope.

In CMake, you can use a pair of `function/endfunction` commands to define a function.

```cmake
function(doubleIt VALUE)
    math(EXPR RESULT "${VALUE} * 2")
    message("${RESULT}")
endfunction()

doubleIt("4")  # prints: 8
```

Unlike macros, functions run in their own scope. None of the variables defined in a function pollute the caller’s scope. If you want to return a value, you can pass the name of a variable to your function, then call the set command with the special argument `PARENT_SCOPE`:

```cmake
function(doubleIt VARNAME VALUE)              # VARNAME is a variable in the global scope
    math(EXPR RESULT "${VALUE} * 2")
    set(${VARNAME} "${RESULT}" PARENT_SCOPE)  # set the named variable in caller's scope
endfunction()
```

Functions also accept an arbitrary number of arguments in the same way that macros do.

Both macros and functions can use the `return()` statement to exit early, but they do not return a value, instead, they typically modify one or more variables that are passed in as arguments. For example, `macro(foo outvar invar)`.

---

CMake variables are defined at file scope. The `include` command executes another CMake script in the __same scope__ as the calling script. It’s a lot like the `#include` directive in C/C++. It’s typically used to define a common set of functions or macros in the calling script. It uses the variable `CMAKE_MODULE_PATH` as a search path.

The `find_package` command looks for scripts of the form `Find*.cmake` and also runs them in the same scope. Such scripts are often used to help find external libraries. For example, if there is a file named `FindSDL2.cmake` in the search path, `find_package(SDL2)` is equivalent to `include(FindSDL2.cmake)`. (Note that there are several ways to use the `find_package` command – this is just one of them.)

CMake’s `add_subdirectory` command, on the other hand, creates a __new scope__, then executes the script named `CMakeLists.txt` from the specified directory in that new scope. You typically use it to add another CMake-based subproject, such as a library or executable, to the calling project. The targets defined by the subproject are added to the build pipeline unless otherwise specified. None of the variables defined in the subproject’s script will pollute the parent’s scope unless the `set` command’s `PARENT_SCOPE` option is used.

So that means a child `CMakeLists.txt` has its own scope and it cannot see variables defined in the parent `CMakeLists.txt`? NO. To make it clear, when `add_subdirectory` is executed, it creates a separate scope to process the child `CMakeLists.txt` and creates a __copy__ of all parent variables to the newly created scope, so the child `CMakeLists.txt` still sees the variable __values__ defined in the parent level, but they are no longer the same variables, just copies. If you need to update a parent variable from the child CMakeLists.txt, you must use the `PARENT_SCOPE` option like this:

```cmake
set(A "Child" PARENT_SCOPE)  # tells CMake to update the original A variable in the parent scope
```

In other words, unless the `PARENT_SCOPE` option has been specified, when setting a parent-level variable in a subdirectory it overrides the value in that scope and any deeper subdirectories. Don’t forget that functions also create a new scope.

Well, now we know `PARENT_SCOPE` sets a variable into the parent scope, but there’s another scope-related option called `CACHE` which sets the variable in the `CMakeCache.txt`, this effectively sets the variable in all scopes.

!!! warning

    Unlike C-based languages, CMake’s loop and control flow blocks do not have their own scopes. Variables set inside conditional blocks or loops persist after the `endif()/endwhile()/endforeach()`.

A CMake script defines targets using the `add_executable`, `add_library` or `add_custom_target` commands. Once a target is created, it has properties that you can manipulate using the `get_property` and `set_property` commands. Unlike variables, targets are visible in every scope, even if they were defined in a subdirectory. All target properties are strings.

```cmake
add_executable(MyApp "main.cpp")                           # create a target named MyApp
get_property(MYAPP_SOURCES TARGET MyApp PROPERTY SOURCES)  # get the target's SOURCES property and assign it to MYAPP_SOURCES
message("${MYAPP_SOURCES}")                                # prints: main.cpp
```

Other target properties include `LINK_LIBRARIES`, `INCLUDE_DIRECTORIES` and `COMPILE_DEFINITIONS`. Those properties are modified, indirectly, by the `target_link_libraries`, `target_include_directories` and `target_compile_definitions` commands. At the end of the script, CMake uses those target properties to generate the build pipeline. There are properties for other CMake entities, too. There is a set of [directory properties](https://cmake.org/cmake/help/latest/manual/cmake-properties.7.html#properties-on-directories) at every file scope. There is a set of [global properties](https://cmake.org/cmake/help/latest/manual/cmake-properties.7.html#properties-of-global-scope) that is accessible from all scripts. And there is a set of [source file properties](https://cmake.org/cmake/help/latest/manual/cmake-properties.7.html#properties-on-source-files) for every C/C++ source file.

---

Arguments in CMake can be difficult at first. Previously we talked about named arguments, which are also called the positional arguments or required arguments, but there’s also the so-called keyword arguments. Keyword arguments use specific predefined ALL-CAPS keywords to separate arguments, each keyword can take no arguments, one argument, or a list. You already see the `PARSE_ARGUMENTS` macro in rez, and you know the examples I’ve written there. But keyword arguments are ubiquitous in CMake built-in commands as well, the only way to master them is to look at the documentation.

CMake offers boolean operator for string comparisons, such as `STREQUAL` for string equality, and for version comparisons, such as `VERSION_EQUAL`.

---

To create a list of lists, you make a list of variable names that refer to other lists.

```cmake
set(list_of_lists a b c)
set(a 1 2 3)
set(b 4 5 6)
set(c 7 8 9)
```

and this is how you can iterate through the list of lists

```cmake
foreach(list_name IN LISTS list_of_lists)
    foreach(value IN LISTS ${list_name})
        message(${value})
    endforeach()
endforeach()
```

---

CMake has a list of predefined directory variables, must remember. Best practice - as a rule of thumb, you should always create a `build` folder under project root first, then run `cmake` command in the build folder, never run `cmake` in the project root.

| Variable                   | Description                                                          | Example Path          |
|----------------------------|----------------------------------------------------------------------|-----------------------|
| `CMAKE_INSTALL_PREFIX`     | Where the build products will be installed to                        | `/usr/local/bin`      |
| `CMAKE_SOURCE_DIR`         | Top level project root folder, your top level CMakeLists.txt is here | `…/myapp`             |
| `CMAKE_BINARY_DIR`         | Top level project binary folder                                      | `…/myapp/build`       |
| `CMAKE_CURRENT_SOURCE_DIR` | Source folder of the current CMakeLists.txt                          | `…/myapp/mylib`       |
| `CMAKE_CURRENT_BINARY_DIR` | Binary folder for the current CMakeLists.txt                         | `…/myapp/build/mylib` |


Modern CMake are structured around targets and dependencies, not build flags, so you are not supposed to use a lot of custom defined variables. The whole family of CMake commands `target_*` can be used to express chains of dependencies and is much more effective than keeping track of state with variables. To create a target from source code, use `add_executable()` and `add_library()`. Then to configure the target, we use properties. Properties further determine the specific details of how CMake builds a target, such as compile flags and link libraries. The most common ones are:

| CMake Property              | Scope                     | Description                                                                                                        |
|-----------------------------|---------------------------|--------------------------------------------------------------------------------------------------------------------|
| `COMPILE_DEFINITIONS`       | Directory, Target, Source | List of preprocessor macros to define when compiling the code                                                      |
| `COMPILE_OPTIONS`           | Directory, Target, Source | List of compiler flags to use when compiling the code                                                              |
| `INCLUDE_DIRECTORIES`       | Directory, Target, Source | List of directories to add to the include path                                                                     |
| `INSTALL_RPATH`             | Target                    | rpath                                                                                                              |
| `LINK_LIBRARIES`            | Target                    | List of other libraries (targets or file paths) that the target should be linked to                                |
| `OUTPUT_NAME`               | Target                    | Use this if you want the built executable or library to have a different name than its CMake target                |
| `POSITION_INDEPENDENT_CODE` | Target                    | Controls whether the code will be built as position independent, which is required when compiling shared libraries |
| `SOURCES`                   | Target                    | The source files configured for a target                                                                           |



[this](https://cmake.org/cmake/help/latest/manual/cmake-properties.7.html) is the full list of properties in CMake (but 90% of them are barely used). As you see, properties have scope, they can be set on a number of different levels:

- Global - affects the entire project
- Directory - affects the current directory and all sub-directories
- Target - only affects a specific target
- Source - affects a specific source file in all targets it’s present in

Use `target_link_libraries()` to link targets (dependencies), this allows the target to reference code stored in the given libraries.

Many target properties come in 2 types/versions: private and interface.

- A private property only affects the target it is set on, e.g. `COMPILE_DEFINITIONS`. They are only used to compile the current target into binary, so that’s an implementation detail, consumers of this target don’t care these private properties.
- An interface property affects every other target that links to this target, e.g. `INTERFACE_COMPILE_DEFINITIONS`. Interface properties are used to carry dependencies between targets, these are called __Usage Requirements__ that consumers of this target must follow in order to work properly.
- So does that mean if A links to B, then A also needs to check all the interface properties in B and copy paste them to A’s own properties list? No. Link dependencies are transitive, meaning that linking will also pull in the interface options of the libraries being linked, and this is recursive. So if A links to B and B links to C, then CMake will automatically link A to C as well, pulling in all the interface properties from C to A, so we don’t need to do it manually.
- If A links to B (so A is a customer of B), the author of B must make sure that B is properly configured in the sense that A (and any other customer) doesn’t need to look at how target B is configured, because that’s an implementation detail of B that other customers should not care about. If the author of B failed to do so, target B would be an ill-formed dependency, the project would be unmaintainable and there’s no way to enforce a modular design. For example, you are a library writer and you created a library called Y, where the public API in header files requires an include path `/foo/include`, if you’ve only added `/foo/include` to target Y’s `INCLUDE_DIRECTORIES` property, then another library X which depends on Y will not be able to compile without manually adding `/foo/include` to its own `INCLUDE_DIRECTORIES` property, and this breaks the modular rule. To avoid this, target Y must add `/foo/include` to its `INTERFACE_INCLUDE_DIRECTORIES` property instead, target X should not need to know how Y works.
- In summary, modern CMake requires that each library defines its own usage requirements properly so they are passed transitively to other targets as necessary.

So how do we set the properties then? Use commands that leverage __usage requirements__ as listed below, do not use commands at the directory or global scope.

```cmake
target_compile_definitions()
target_compile_options()
target_include_directories()
target_link_directories()
target_link_options()
target_precompile_headers()
target_sources()
```

There are 3 keywords for setting target properties in a command:

- `PRIVATE` - only sets the private version of the property, e.g. `COMPILE_DEFINITIONS`
- `INTERFACE` - only sets the interface version of the property, e.g. `INTERFACE_COMPILE_DEFINITIONS`
- `PUBLIC` - sets both the private and interface version of the property, e.g. `COMPILE_DEFINITIONS` + `INTERFACE_COMPILE_DEFINITIONS`

Cache variables are special variables that keep their values between invocations of CMake. These variables are persistent across calls to `cmake` and available to all scopes in the project. Modifying a cache variable requires using a special form of the set function: `set(<variable> <value>... CACHE <type> <docstring> [FORCE])`.

`CMAKE_BUILD_TYPE` has 4 standard build types: `Debug`, `Release`, `RelWithDebInfo` and `MinSizeRel`. To set this variable, use `-DCMAKE_BUILD_TYPE=Release` command option for example. The main purpose of this variable is to control which compile flags are used.

Generator expression are introduced in CMake 3.15, don’t use them if you are running an older version.

`BUILD_INTERFACE` is a generator expression used in target properties that allows specifying include directories or compile definitions only when building a target. It is commonly used to specify header-only dependencies that are not needed at runtime.

For example, the following code adds the include directory `./include` to the target `mylib` only when building the target, once it’s already built into a binary, running it at runtime does not need that include path anymore.

```cmake
target_include_directories(mylib
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)
```

Another example, the following code sets compile options for the target `mylib` only when the target is being built, not when it is installed. Once it’s already built into a binary, consumers of `mylib` should not inherit these warning flags.

```cmake
target_compile_options(mylib
  INTERFACE
    "$<BUILD_INTERFACE:-Wall;-Wextra;-Wshadow;-Wformat=2;-Wunused>"  # must be quoted since we have semicolons in the argument
)
```

In general, `BUILD_INTERFACE` is used to specify include path or compiler flags that are only needed during the build process, while `INSTALL_INTERFACE` is used to specify things that are needed both during the build process and during installation.

---

In CMake, an interface library is a special type of library that defines a set of requirements for linking against it. Unlike traditional libraries that contain actual object code, an interface library only specifies a list of headers and required linker flags. Interface libraries are useful when you have a set of requirements that multiple other libraries or executables share. Instead of duplicating the same requirements across all targets, you can define them once in an interface library and let the dependent targets link against it. Header-only libraries is a common example of an interface library, but an interface library doesn’t even need to have header files or any code, it could just be a code-less target with only usage requirements.

To create an interface library in CMake, you can use the `add_library()` command with the `INTERFACE` keyword. Here is an example:

```cmake
add_library(A INTERFACE)
target_include_directories(A INTERFACE include)
target_link_libraries(A INTERFACE pthread)
target_compile_features(A INTERFACE cxx_std_11)
```

Then, any target that links against A will inherit these requirements.

---

Build vs Install - "build" refers to the process of compiling the source code and linking the object files to create the target binary, whereas "install" refers to the process of copying the binary files to a specified location on the system, typically in order to make them available to other programs or users. Compared with “build”, specifying install rules is much easier using the `install()` command.

```cmake
install(TARGETS XXX DESTINATION bin)
install(FILES XXX.h DESTINATION include)
```

In graphics and rendering, we often use the term “artifacts” to describe anomalies apparent during visual representation as in digital graphics and other forms of imagery, those are the visual artifacts or rendering artifacts that should not appear if everything works correctly, they signal that something is wrong. However, the official definition of “artifacts” merely refers to things made by human/artists, things that are not natural. In software engineering, a software artifact is an item that is produced during the development process, it could be any intermediate or final output produced during the software build process. In CMake or other build tools, “build artifacts” are the files generated by a build process, including the executable files, libraries, object files, configuration files, documentation, and any other files needed to run or distribute the software.

For every target in the project, CMake will create a subfolder `<target>.dir` under `CMakeFiles`. The intermediate object files are stored in these folders, together with compiler flags and link line.

---

When debugging CMake, how to print out the value of a variable? - You can use the `message()` command, but it’s not user-friendly nor pretty, instead you should use:

```cmake
include(CMakePrintHelpers)
cmake_print_variables(var1 var2 ... varN)
```

In CMake, you can run custom commands at configure-time (when CMake is parsing your `CMakeLists.txt` file) prior to build system generation. This is achieved with the `execute_process` command which explicitly runs one (or more) child process(es) when invoking the cmake command. https://cmake.org/cmake/help/latest/command/execute_process.html How can this be useful? - Well, it’s super useful, for example, we can use `execute_process` to check whether a module or library is installed on our computer before building occurs, we can use `execute_process` to resolve a rez environment first so that building process can find all the packages, etc. You can also use `execute_process` to run checks on our compilers and linkers, or check whether a certain library can be used correctly before attempting to build our own artifacts, but CMake already provides modules and commands for these purposes so you should directly use these: `check_cxx_compiler_flag`, `check_cxx_source_compiles`, etc.

What if we want to perform some specific actions depending on targets (not configure-time anymore)? - In this case, we can use `add_custom_command` to add custom commands to a target, these commands can be executed before linking (with `PRE_BUILD` and `PRE_LINK`) or after (with `POST_BUILD`). That’s also how rez implements its `pre_*` and `post_*` commands in package.py.

!!! tip

    For large projects with many targets, we can visualize the dependencies between the targets with Graphviz:

    ```cmake
    $ cd build
    $ cmake --graphviz=myapp.dot ..
    $ dot -T svg myapp.dot -o myapp.svg
    ```

    The visualization can help you quickly reason about the dependencies within your project.


With the advent of CMake 3.0, also known as Modern CMake, there has been a significant shift in the way the CMake domain-specific language (DSL) is structured. Rather than relying on variables to convey information in a project, we should shift to using targets and properties. A target is declared by either `add_executable` or `add_library`. Each target has properties, which can be read with `get_target_property` and modified with `set_target_properties`. Compile options, compile definitions, include directories, source files, link libraries, and link options are common properties of targets. It is much more robust to use targets and properties than using variables. Using targets, you can achieve granular control over how artifacts are built and how their dependencies are handled. Get away from the legacy old-school CMake! (before v2.8)

```cmake
target_link_libraries(A
  PRIVATE B
  INTERFACE C
  PUBLIC D
)
```

- `PRIVATE` - B will only be used to build A but not be propagated as a dependency to other targets consuming A.
- `INTERFACE` - C will only be propagated as a dependency to other targets consuming A.
- `PUBLIC` - D will be used to build A and will also be propagated as a dependency to any other targets consuming A.

You can get the current value of any property with `get_property` and set the value of any property with `set_property`, these are mainly used for properties not in the target scope.

OK, targets and properties are great, but how do I set up a target that is a header-only library? - Use only the `INTERFACE` visibility keyword!

```cmake
add_library(mylib INTERFACE)
target_include_directories(mylib INTERFACE include)
target_link_libraries(mylib INTERFACE Boost::Boost)
```

CMake offers a family of commands to find artifacts installed on your system - `find_file`, `find_library`, `find_package`, `find_path`, `find_program`. The workhorse of dependency discovery is `find_package`, which will cover your needs in almost all use cases.

`find_package` will attempt finding the package with name `<PackageName>` by searching in a number of [predefined folders](https://cmake.org/cmake/help/latest/command/find_package.html?highlight=find_package#search-procedure). It is possible to ask for a minimum or exact version. If `REQUIRED` is given, a failed search will trigger a fatal error. The rules for the search are obtained from modules named `Find<PackageName>.cmake`. You should only use the other commands in the `find_*` family in very special, very narrow circumstances.

Why we should only use `find_package` in modern CMake? Because it will set up imported targets: targets defined outside your project that you can use with your own targets. The properties on imported targets defines usage requirements for the dependencies. This means that when you `target_link_libraries` to link an external target discovered by `find_package`, the compiler flags, definitions, include directories, and link libraries from that external target will propagate to your own target as well.

When attempting dependency detection with `find_package`, you should make sure that:

- A `Find<PackageName>.cmake` module exists,
- Which components, if any, it provides, and
- What imported targets it will set up.

Where to acquire this information? - https://cmake.org/cmake/help/latest/manual/cmake-modules.7.html#find-modules for example, from https://cmake.org/cmake/help/latest/module/FindBoost.html you can see that `find_package(Boost)` will set up a `Boost::boost` imported target for header-only dependencies (Boost include directory), use that as the argument to `target_link_libraries`. Here’s another example that will pull in all the usage requirements from OpenMP to your own target.

```cmake
find_package(OpenMP 4.5 REQUIRED COMPONENTS CXX).
target_link_libraries(task-loop PRIVATE OpenMP::OpenMP_CXX)
```

What to do when there is no built-in `Find<PackageName>.cmake` module for a package you depend on? e.g. Pixar USD? - That’s a hard question, I still need time to figure out.

What if you want to compile Python wrappers to C++ in your project? - Use pybind11, it is a header-only library and has excellent integration with CMake.

---

In CMake, an "imported target" is a target that is not built by the current CMake project, but is provided by an external source, such as a system library or a library built by another CMake project. An imported target can be used as a dependency of other targets, and CMake provides several commands to configure the usage of imported libraries, such as `find_package()` and `target_link_libraries()`.

An "interface library" is a special type of CMake library target that only defines an interface and does not build any code. It can be used to specify dependencies and other properties that are required by other targets, without actually building any code.

An “alias target” is a way to create a new target name that refers to an existing target. This can be useful for creating shorter or more convenient target names or for creating different configurations for the same library. To create an alias target, you can use the `add_library()` command with the `ALIAS` option, followed by the name of the alias and the name of the target it should refer to. For example:

```cmake
add_library(mylib mylib.cpp)
add_library(mylib_alias ALIAS mylib)
```

An alias target is effectively just a synonym, so it is read-only and non-modifiable. You can not use `set_target_properties` on an alias target.

---

CMake tips and tricks?

- Do not glob patterns (e.g. all files that end with `*.cpp`) when defining targets, instead, list them explicitly, otherwise CMake can have trouble tracking dependency changes when you add files after you have configured.
- Do not collect all sources in one file, every subfolder deserves its own `CMakeLists.txt` for maintainability.
- Avoid variables with parent or global scope. Prefer functions over macros. Encapsulate and prefer separation of concerns.
- Always run `cmake` or `ccmake` in the build folder.
- Treat CMake code like production code and version control them. Do not version control the build files or make files.
- Define project-level properties globally. For example, a project might use a common set of compiler warnings. Defining such properties globally in the top-level `CMakeLists.txt` file prevents scenarios where public headers of a dependent target causing a depending target not to compile because the depending target uses stricter compiler options. e.g. `add_compile_options(-W -Wall -Werror)`.
- In modern CMake, forget the commands `add_compile_options`, `add_definitions`, `include_directories`, `link_directories`, `link_libraries`, etc. Those commands operate on the directory level rather than on the target scope, so all targets defined on that level inherit those properties which increases the chance of hidden dependencies.
- Instead of setting `CMAKE_CXX_FLAGS`, it’s much better to tell CMake the compile features and let it figure out the appropriate compiler option to use.
- Don’t understand targets and properties and the visibility levels and propagation rules? Think in terms of OOP! A target is just an object, and the properties are its member variables. Similarly, `add_executable` and `add_library` are the class constructors, `set_target_property`, `get_target_property` and the `target_*` family of commands are member functions.
- Always use visibility keywords `PUBLIC`, `PRIVATE` and `INTERFACE` in the `target_*` family of commands.
- Do not abuse `target_compile_options` to declare compile options that affect the ABI. Those options should be declared globally using the old-school `add_compile_options` as they have nothing to do with the target.
- Don’t use `target_include_directories` with a path outside your module. That breaks the rule. Instead, properly specify the dependencies via `target_link_directories` to propagate include directories as usage requirements.
- Use `cmake_parse_arguments` as the recommended way to handle complex argument-based behaviors or optional arguments in any function.
- Finally this is a C++ tip - For each header file, there must be an associated source file that `#includes` the header file at the top, even if that source file would otherwise be empty. This helps keep the source tree clean and complete, otherwise most analysis tools cannot analyze the header file alone and report diagnostics.



Deep industry talks:

- https://www.youtube.com/watch?v=bsXLMQ6WgIk, https://github.com/boostcon/cppnow_presentations_2017/blob/master/05-19-2017_friday/effective_cmake__daniel_pfeifer__cppnow_05-19-2017.pdf
- https://www.youtube.com/watch?v=m0DwB4OvDXk, https://github.com/CppCon/CppCon2019/blob/master/Presentations/deep_cmake_for_library_authors/deep_cmake_for_library_authors__craig_scott__cppcon_2019.pdf

Now you should be much more comfortable reading the [official documentation](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html#target-usage-requirements) for a deeper exploration


When CMake is mixed with Rez…

```cmake
if(COVERAGE)
	ADD_DEFINITIONS(-pg -fprofile-arcs -ftest-coverage)
	SET_GLOBAL_LINKER_CXX_FLAGS(-fprofile-arcs)
endif(COVERAGE)
```

- `ADD_DEFINITIONS` is a CMake native command that adds definitions to the compilation command line for source files. In this case, `-pg`, `-fprofile-arcs`, and `-ftest-coverage` are added as definitions (compiler flags).
- `-pg` is a compiler flag used for profiling the code. When this flag is used, the compiler generates profiling information that can be used to determine the execution time of different functions in the program. For example, the `gprof` profiling tool can use this profiling information to determine which functions in a program take the most time to execute.
- `-fprofile-arcs` and `-ftest-coverage` are compiler flags used for code coverage analysis. These flags instrument the code with probes that record how many times each line of code is executed during the program's execution. The information is then used to generate a report that shows which lines of code were executed and which were not.
- `-fprofile-arcs` is also a linker flag. `SET_GLOBAL_LINKER_CXX_FLAGS(-fprofile-arcs)` tells the linker to generate code coverage information as well.

These flags are often used together to generate profiling and coverage information for the program when it is compiled and executed. That’s what this code block does. To enable it, add a line `set(COVERAGE TRUE)` to your `CMakeLists.txt` file before it imports `include(RezBuild)`, alternatively, add an extra command line option, i.e. `cmake -DCOVERAGE=TRUE ...`






