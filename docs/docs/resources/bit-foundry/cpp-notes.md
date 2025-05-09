



# C/C++


## Style Guide

- Code editor - MonoLisa font, line spacing 1.2
- Soft wrap at 120 characters

### Preprocessor directives

Include headers - user-defined headers should appear after C/C++ library headers.

```cpp
#include <cstdlib.h>  // C library headers have the ".h" extension, C++ library headers do not
#include <iomanip>    // standard library or external headers typically use brackets
#include "class.h"    // user-defined headers use double quotes
```

Use `SCREAMING_SNAKE_CASE` for macro names.

```cpp
#define MAX_VALUE 100  // just an example, should use constants in practice
#define CALC_SQUARE(x) ((x) * (x))
```

### Comments

Avoid using block comments, they are dangerous!

```cpp
/* the 2nd block comment will fail
std::cout << "Hello";  /* the 1st block comment */
std::cout << "World";
*/
```

Prefer doc comments over block comments, some IDEs have special rendering for doc comments.

```cpp
/// doc comment style 1
//! doc comment style 2
```

However, do note that:

- Doc comments are not comments but documentation, they often apply to public modules, classes and functions, the target audience is the API user, it’s about how to use the code.
- Comments describe how the code internally works, it’s intended for the developer.
- Other than documentation, avoid writing comments as best as you can.
- Instead of writing comments, refactor your code so that the code itself clearly conveys the intention.
- Use good variable names and function names to make them obvious and self-explanatory.
- For complex conditions or block of statements, move them into a separate function that’s clearly named.

Write comments if:

- The code does something non-obvious for performance reasons.
- It’s a tricky part in an algorithm that cannot be explained by the algorithm’s function name.
- You are referencing to some math or algorithms online, also put links to the sources in your comment.

Besides, a lot of info is already contained in the type so there’s no need to write comments. For example, a shared or unique pointer implies the ownership so you must take the responsibility of destructing it properly, whereas a raw pointer implies that we should only use it to do simple checks or invoke a const member function that doesn’t mutate the underlying object. Likewise, a std::optional return type indicates that we need to handle exceptions in case it doesn’t return a value, etc.

### Namespaces

Namespace names should be all lower case, abbreviated to be short, and use `snake_case` if necessary.

```cpp
namespace std {}
namespace mana {}
namespace core { namespace rdr {} }  // "renderer" abbreviated to "rdr" for cleanliness

using namespace pxr;
using namespace glm;
using namespace boost::math;
using namespace core::rdr;
```

Some external libraries do not follow this convention. In that case, use a macro to wrap it around.

```cpp
#define imgui ImGui
#define oiio OIIO  // OpenImageIO
#define ocio OCIO  // OpenColorIO
```

Every top level namespace (unless anonymous) should have a list of corresponding macros for convenience. Within the `OPEN_SCOPE` and `CLOSE_SCOPE macros`, we can save an indentation level (4 spaces) on every line! This leaves us with a very clean indentation scheme overall.

```cpp
#define MANA_NAMESPACE_OPEN_SCOPE namespace mana {
#define MANA_NAMESPACE_CLOSE_SCOPE }
#define MANA_NAMESPACE_USING_DIRECTIVE using namespace mana;

MANA_NAMESPACE_OPEN_SCOPE
...
MANA_NAMESPACE_CLOSE_SCOPE
```

### Naming things is hard

For naming variables in general

- Do not use abbreviations unless they are well-known, use meaningful and descriptive English words.
- Using descriptive natural language words improves not only readability, but also auto code completion.
- Use camelCase for global and local variables. (static and extern variables? maybe)
- Use SCREAMING_SNAKE_CASE for constants.
- Do not use legacy Hungarian notation (putting types or properties into the variable name).
- Put units into variable names (e.g. timeoutInSeconds) unless the type already includes the units.

For naming classes and structs

- Use PascalCase for all classes and structs.
- Use a generic name for the base class, don’t add Base, e.g. class Truck instead of class BaseTruck.
- Use an over-specified name for the derived class, e.g. class TrailerTruck instead of class Truck.
- Class names can be adjectives, e.g. class Movable, class Hittable.
- Don’t emphasize an interface or abstract class, e.g. class Hittable instead of class IHittable.
- Never create a utility/helper class or namespace, it’s indicative of a bad design. Instead, think carefully where they really belong to and sort them into the right modules.

For naming member variables in a class/struct

- In C++, any identifier beginning with an underscore _ is reserved to the implementation.
- Any identifier that contains a double underscore __ anywhere is reserved to the implementation.
- Therefore, you can never use any leading _ or use double __ anywhere in the code.
- Do not use the m_ prefix for member variables in a class or any other prefix like that (old school).
- Instead, suffix private and protected members with a trailing underscore _ (not leading _).
- From developer’s point of view, there’s no need to differentiate private and protected members.
- Public and static member variables do not need any prefix or suffix, just use normal naming convention, if you find it difficult to distinguish between them, you need a better IDE, not another naming style.

For naming functions including member functions

- As mentioned, use any leading `_` or use double `__` anywhere in the code.
- Prefer camelCase over PascalCase, do not capitalized the initial character, like `main()`.
- No, let’s follow what USD does, use PascalCase…………………………………………………………………..
- Getters (accessors) do not start with get, e.g. `settings()` instead of `getSettings()`.
- Setters must start with set, e.g. `setModel()`.
- For private and protected member functions, start the function name with do, e.g. `void doUpdateNode()`.
- Again, there’s no need to differentiate private and protected member functions.
- C++ standard library uses the old `snake_case` convention for function names, like `emplace_back()`, this is not consistent with our style, but it’s actually desired since we can tell which one is our own function.
- USD and Hydra uses PascalCase for function names which isn’t consistent with our style either, but it’s actually desired for the exact same reason.

### Where should I put the `*&[]` characters?

Ampersand and asterisk should immediately follow the type, rather than preceding the variable name.

```cpp
float* fptr;
float& fref;
int* func(const void* vp) {}
int& func(const std::vector<T>& vec) {}
```

Never declare two pointers on the same line, declare them on separate lines.

```cpp
int *number1, *number2;  // nope, this breaks our rule
const int* number1;
const int* number2;
```

Square brackets should follow the array name, not the type.

```cpp
float pixels[1920 * 1080];
vec3 points[256];
```

### Where should I put the `{}` curly braces?

This is the formatting style that’s totally up to your personal preference as well as the use case. Do not overemphasize “consistency” here, that’s absolutely bullshit. What really matters here is readability, cleanliness and clarity, it’s not something like the naming convention that you need to pick one and consistently stick to it throughout the entire codebase.

If you always put curly braces on a new line, the code will be super bloated. If you always put curly braces on the same line, it can be hard to read. So no one is better than the other. Instead do this:

- if you have many statements to enclose inside, curly braces should be on a new line.
- if there’s only 1 or 2 lines, packing them closely together will look nicer.

For example, braces at the namespace, class or function level are typically on a new line, but as for braces following an if-else statement, a loop or a catch block, it depends on the complexity of that code block.

```cpp
enum class Color { Red, Green, Blue };  // clear enough on one line

enum class Fruit
{
    Pineapple,
    Orange,
    Strawberry,
    Grapefruit,
    Banana
};
```

```cpp
void DoWork(const Bar& bar)
{
    for (unsigned int i = 0; i < animation->numOfChannels; ++i)
    {
        aiNodeAnim* channel = animation->channels[i];
        std::string bone = channel->nodeName.c_Str();

        auto node = ranges::find_if(nodes, [&bone_name](const Node& node) {
            return node.name == bone_name;
        });

        // open curly stays on the same line
        if (node == nodes.end()) {
            continue;
        }

        // open curly starts on a new line
        if (node.isValid())
        {
            Channel& channel = channels[node->bid];
            CORE_ASERT(channel.bone_id < 0, "This channel is already filled, duplicate bone!");
            channel = std::move(Channel(ai_channel, bone_name, node->bid, duration));
            nodes[node->nid].alive = true;
            n_channels++;
        }
    }

    try {
        std::vector<int> vec{3, 4, 3, 1};
        int i{vec.at(4)};
    }
    catch (const std::out_of_range &e) {
        std::cerr << "Accessing a non-existent element: " << e.what() << '\n';
    }
}
```

### Don’t be a nester!

Using deeply nested functions is often a code smell and an indication of bad design.

- Do - limit the number of nested levels to 3 in a function.
- Don’t - have an inner code block nested at level 4+.

There are two ways you can de-nest your function.

- Extraction - pull out part of the function into its own function (can optionally mark as inline).
- Inversion - for if-else statements, flip the conditions and error checks into an early return.

### Abstraction

- Do not overuse abstraction to avoid duplicating code. Abstraction also introduces coupling.
- We need to balance abstraction vs coupling, it’s fine to have some duplication in our code.
- Do not abstract everything away to remove repetition, create a Mixin class if needed.













## Basics Review

Compile, link and run with GCC.

```sh
g++ -o executable.exe code1.cpp code2.cpp -std=c++11
./executable.exe arg1 arg2 ...
./executable.exe < in > out  # read data from "in" and redirect output to "out"
```

Exit status of a C++ executable = return value of the entry point function which is mostly `main()`.

```sh
g++ -o executable.exe main.cpp
./executable.exe
echo $?  # 0/EXIT_SUCCESS for success, failure otherwise
```

The `main()` function:

```cpp
int main(int argc, char** argv) {}
// argc (arguments count) = number of arguments from the command line + 1 (path to the executable)
// argv (arguments vector) stores all arguments as a vector of strings (the executable path is prepended to the vector)
// int main() is the only special function that doens't need to return an int (returns 0 by default)

int main(int argc, char* argv[]) {}
// char* is a pointer to the (const) string literal
// char** or char*[] is a vector of char*
// char** and char*[] are equivalent, both represent vector of strings

int main(int argc, char* argv[], char* envp[]) {}
// envp is another optional argument which contains environment variables
// do not use argv or envp in calls to system(), it is a huge security hole
// for example, system(argv[2]) is bad, argv[2] could be rm -rf *
```

By default, command line arguments are divided by spaces. If we want an argument to include a space, it must be typed in double quotes.

```cpp
./executable.exe "hello world" and -a -b -c
// argc = 6
// argv[0] = ./executable.exe
// argv[1] = hello world
// argv[2] = and
// argv[3] = -a
// argv[4] = -b
// argv[5] = -c
```

### Compiled vs Interpreted languages

Compiled languages such as C, C++, C#, Objective-C, Pascal, Scala, Swift, Erlang, Haskell, Rust, PL/SQL and Go, are compiled into machine code that can be executed directly on a computer's processor. A compiler will translate code into computer's "native" language upfront, well before the program is even run. This process can take many passes before it is optimized as machine code, but the output is always machine code that executes efficiently and natively on the platform.

Interpreted languages such as Java, JavaScript, PHP, Perl, Python and Ruby, are not already in "machine code" prior to runtime. Unlike compiled languages, an interpreted language's translation doesn't happen beforehand. Translation occurs at the same time as the program is being executed. Interpreted languages have a major advantage: they are portable, which means they can run on different operating systems and platforms.

### Primitive types (POD = plain old data)

```cpp
char x;  // 1 byte = 8 bits
int x;   // 4 bytes = 32 bits

// a type can be signed or unsigned
char a; unsigned int b;

// for signed integers, all numbers with the most significant bit equal to 1 are negative, this encoding is called two's complement
// e.g. binary (1011) = -(1 * 2^3) + (0 * 2^2) + (1 * 2^1) + (1 * 2^0) = -5 in decimal
// to represent negative X, take the bits for X, flip them (turn 0s into 1s and 1s into 0s) and then add 1
// e.g. number 5 (0101) -> flip the bits (1010) -> add 1 (1011) = -5

short int               // 2 bytes = 16 bits
long int                // 4 bytes or 8 bytes depending on the architecture
long long int           // 8 bytes = 64 bits, -(2^63) to (2^63)-1
unsigned long long int  // the biggest int type in standard C++, hold numbers up to 18,446,744,073,709,551,615

// using fixed width integer types, size of the data type is much clearer
uint8_t
int16_t
uint32_t
int64_t
char32_t  // utf-32
...

// boolean type is 1 byte even though we only need 1 bit for 0/1, other 7 bits are wasted
// there are cool techniques to store 8 booleans in one byte though
bool x = 1;  // 1 byte = 8 bits

// floating point numbers are represented using scientific notion in base 2 (IEEE Standard)
// the most significant bit is the sign bit, next 8 bits encode the exponent, lowest 23 bits encode the mantissa
// the formula is: (-1)^s * m * 2^e, where m: mantissa or significand, e: exponent
// when s = 1, the number is negative. when s = 0, the number is positive.
// float only has single precision, they are approximate and imprecise so do not check == equality on it
float x = 32.6f;  // 4 bytes

double 	     // 8 bytes, double precision, there's no half float type in C++
long double  // 12 bytes = 96 bits
wchar_t 	 // 2 or 4 bytes, 1 wide character

sizeof(int)  // sizeof() returns the size (number of bytes) of a type/variable/expression
sizeof(obj)  // result of sizeof() might differ depending on the compiler/platform (32-bit or 64-bit architecture)
```

### C vs C++ output

```cpp
printf();        // C style
sprintf();       // C style
std::cout << 0;  // C++ style
std::format();   // the preferred way in C++20 and above

std::cout << "Hello\n";             // \n only starts a new line but does not flush output
std::cout << "Hello" << std::endl;  // std::endl starts a new line and flushes the output
```

How to pause a program and wait for a keyboard input to continue?

```cpp
system("pause");  // BAD, platform-specific hack, unsafec
std::cin.get();   // GOOD
```

Infinite loops, use `Ctrl+C` to break

```cpp
for (;;) {}
while (true) {}
```

Pass a function as an argument of another function

```cpp
float f(int x) {
    return x + 1;
}

int g(float (*f)(int), int a) {  // the address of f() will be passed to g()
    return (*f)(a);  // extract (*f) before calling f(a)
}

int main() {
    g(f, 1);  // pass the function name, which is the same as the function address
}
```

Caveat of deep copy - if a class has pointers or any runtime allocation of resources like a file handle, a network connection, etc, we must define our own copy constructor to make a deep copy, which means that pointers (or references) of copied object point to new memory locations.

Why we should not use using `namespace std;`? because it can easily cause duplicate names.

Array as a function argument:

C++ does not allow passing an entire array as an argument to a function. However, You can pass a pointer to an array by specifying the array's name. When the function is called, array arguments are implicitly adjusted to pointer arguments, so `func(int a[])` is equivalent to `func(int* a)` as `int a[]` is adjusted to `int* a`. Note however that `int a[10]` is not equivalent to `int* a`. In fact, when we pass the array's name as an argument to the function, what's really being passed is the address of the array, and this call is similar to call by reference. As a result, if we have mutated the array inside the function's body, this change will also be applied to the real array outside the function.

The address of the array is the address of its first element, which specifies the start position of the array, but not the length, that's why we always pass the array's length "n" as an extra argument. To ensure "n" is non-negative and large enough to hold a possibly very long array, use `size_t` as its type. `size_t` is an unsigned int with the right number of bits to describe the size or index of an array, it could be unsigned int or unsigned long depending on your compiler and OS platform.

When using raw arrays in C++, we often need to maintain the size of the array ourselves, there’s not a `size()` method as in other languages. Although there’s a trick `sizeof(a) / sizeof(int)` for checking the size of an array, it is not reliable.

```cpp
void func1(int a[10]) {  // sized, NOT equivalent to func1(int* a)
    ...
}

void func2(int a[]) {  // unsized, equivalent to func2(int* a)
    ...
}

void func3(int b[][4]) {  // 2-dimensional array
    ....
}

int a[10];
int b[3][4];

func1(a);  // pass array's name directly to the function call
func2(a);  // array's name can be used as a pointer (but not essentially a real pointer)
func3(b);
```

if the array argument is unsized, C++ will not perform any boundary checks. In this case, we must pass the array size as a supplementary argument

```cpp
void sort(int data[], int length) {}
double average(int arr[], int size) {}
```

C style strings - arrays (mutable), memory address on the stack

```c
char string[] = {'H','e','l','l','o','\0'};  // essentially it's a char array
char string[] = "Hello";  // as a shorthand, we can write like this
string[0] = 'w';  // the string is mutable because arrays are mutable

char str[11]      // 1 string, length <= 10 (we write 11 because there's an extra '\0' character)
char arr[10][21]  // 10 strings, each has length <= 20 (we write 21 because of the null terminator)
arr[0]  // the 1st string in the array
arr[9]  // the last string in the array

char str[3] = "abc";  // error, because maximum length is 2 but received 3
```

C style strings - pointers (immutable), memory address in literals pool

```c
char* string = "Hello";  // a string literal in the memory pool, it's immutable

std::cout << static_cast<const void*>(string) << std::endl;  // address of string
std::cout << &"Hello" << std::endl;  // address of "Hello" = address of string

string[0] = 'h';  // Segmentation Fault, the string value cannot be mutated
const char* string = "Hello";  // it's a good habit to write const char* since it's immutable
```

Summary of C style strings:

In practice, we prefer to use arrays as C style strings because it's mutable, but this is dangerous and we have to make sure that the array has enough space. C++ does not check array boundaries, if it's out of bound, this will lead to the so-called segmentation fault (trying to access or modify memory that you do not own). On the other side, we also need to care about the caveats of using pointers as C style strings. Even though the `char*` string is immutable, the program still compiles when we attempt to mutate the string, and it is going to crash only at runtime. As a good programming habit, we should always use the `const` keyword before a `char*` string, so that the program will not compile when we try to mutate it.

```c
char* string = "Hello";
string[2] = 'x';  // program will crash immediately at runtime

const char* string = "Hello";
string[2] = 'x';  // program won't compile, we will notice this error at compile time
```

C style strings manipulation - internally, every string ends with `\0`, so `'S'` is not the same as `"S"`, which is actually `'S' + '\0'`.

```c
#include <cstring>

strlen(string);
strcpy(to, from);  // make sure string "to" is long enough to hold "from"
strcmp(s1, s2);    // returns a positve if s1 > s2, a negative if s1 < s2, and 0 if s1 == s2
strcat(s1, s2);    // concat s1 = s1 + s2, make sure s1 is long enough

// must always use strcmp() to compare two strings to see if they are equal
// the == operator only checks if two strings are pointing at the same place (pointer equality)
char str1[] = "Hello";
char str2[] = "Hello";
strcmp(str1, str2);  // returns 0
str1 == str2  // returns false because str1 and str2 have different addresses
strcasecmp(s1, s2);  // this function performs case-insensitive comparison (A == a)

char x;
cin >> x;
int ascii = static_cast<int>(x);  // every char has an ascii value

if (ascii >= 48 && ascii <= 57) { cout << "0-9 digit" }
if (ascii >= 65 && ascii <= 90) { cout << "upper case letter" }
if (ascii >= 97 && ascii <= 122) { cout << "lower case letter" }
```

C++ style strings - the `std::string` class

```cpp
#include <string>   // more convenient and safer than using char[]

std::string input;
cin >> input;  // ok
scanf("%s", &input);  // no, C++ style string does not work with scanf("%s")

std::string str1 = "Hello";
std::string str2 = "World";
std::string str3;

str1[0]  // 'H'
str2[2]  // 'r'
str3 = str1;  // copy
str3 = str1 + str2;  // concat
std::cout << (str1 < str2) << std::endl;  // compare
std::cout << str3.length() << std::endl;  // string length
std::cout << str3.size() << std::endl;  // string length

std::string sub = str1.substr(2,3);  // "llo", substr(pos, length)
str2.insert(5, "Craft");  // "WorldCraft", insert(pos, string)

std::string str4 = "1234567890";
size_t pos = str4.find('5');  // find
if (pos != std::string::npos) {  // npos = -1
    std::cout << "Found at position: " << pos << std::endl;  // pos = 4
}
else {
    std::cout << "Not found!" << std::endl;
}

str4.replace(0, 5, "abcde");  // "abcde67890", replace(pos, length_of_portion, string_to_replace)
```

C style input/output - `scanf()`, `printf()` could cause buffer overflow security problems, which makes your code vulnerable to attacks. However, they are very good at handling formatted input and output, and they are much faster than `cin`, `cout`. Note that some compilers and IDEs such as Visual Studio may not support `scanf()`, you have to add `#define _CRT_SECURE_NO_WARNINGS` at the beginning of the file to use it.

```cpp
#include <cstdio>
#define _CRT_SECURE_NO_WARNINGS

int i, j;
char c;
char s[10];  // make sure scanf() will not overflow
float f;

scanf("%d", &i);
scanf("%c", &c);
scanf("%s", &s);  // "%s" format can only be stored in C style strings
scanf("%f", &f);
scanf("%d %d", &i, &j);  // scan multiple user inputs in one line
printf("%.2f", i);

int year, month, day;
scanf("%d-%d-%d", &year, &month, &day);  // must call by reference(address)
printf("%d-%d-%d", year, month, day);

//! if user input is too long to be held in string[10] -> segmentation fault
char string[10];  // make sure the array is long enough
scanf("%s", &string);
scanf("%s", string);  // this also works because array's name = array's address

// printf() outputs directly to the console, sprintf() outputs to a string variable
char information[100];  // make sure the array is long enough, otherwise segmentation fault
sprintf(information, "%s is a %s. He is %d-year-old.", name, gender, age);
cout << information << endl;

// printf() can be susceptible to security vulnerability, such as format string attacks:
// https://en.wikipedia.org/wiki/Uncontrolled_format_string
printf(userInput);  // risky, what if userInput is "select * from user_roles;" or "rm -rf *" or contains ("%d", password)?
printf("%s", userInput);  // safer

for (int i = 1; i <= 10; i++) {
    printf("%d ",i);
    fflush(stdout);  // without fflush(), will not print to screen at once (saved in buffer)
    sleep(1);
}
```

C++ style input/output - unless you need to handle very complicated input/output formats, or you are concerned about speed and time limit, using `cin`, `cout` is always a better option because they are secure, robust and powerful. Note that `cin`, `cout` is often banned in algorithm competitions for their slowness, but that doesn’t apply to normal C++ programs.

```cpp
cin         // an object of type istream
cout        // an object of type ostream
cerr, clog  // the other two ostream objects

cout << endl;  // "endl" ends the current line and flushes the cout buffer
cout << '\n';  // '\n' also ends the line but does not flush the buffer, take care
cout << '\a';  // beep or alarm

// when you debug with "cout", always add "endl" to flush the stream
// otherwise sth could be left in the buffer and mislead you
cout << var << endl;  // debug mode

cin >> v1 >> v2;  // chain
while (cin >> value)  // test the state of the istream object cin (valid/invalid)

std::string line;
while (getline(cin, line))  // read in a whole line, including spaces
                            // press Enter to input a new line, press Ctrl + Z followed by Enter to finish input
```

Learn more about string streams and file streams in C++.

Void pointer - can later be assigned the value of any other pointers

```cpp
void* vp;
int* p = &"123";
vp = p;  // it's ok to assign any pointer to vp

void* vp;
int* p = &"123";
p = (int*) vp;  // when vp is assigned to other pointers, explicit type conversion is necessary in C++ (not in C)
```

Void pointer is a pointer to an unspecified type of data, it's used to write generic functions in C. However, `void*` is also dangerous, in C++, we prefer to use template `T` for generic functions.

```cpp
int func(const void* vp) {
    const int* p1 = (int*) vp;  // void* can be typcasted to any type
    const char* p2 = (char*) vp;
}

int* x = (int*) malloc(sizeof(int) * n);  // malloc() returns void* which can be typecasted to any type
double* x = (double*) malloc(sizeof(double) * n);
```

Null pointer - a pointer that points to nowhere but the type is already determined.

```cpp
int* ptr = 0;
int* ptr = NULL;     // same as above
int* ptr = nullptr;  // better
double* ptr = NULL;
```

Arrays and pointers - array's name can be used as a pointer which points to the first element in the array. Note however that array's name is not the same as a real pointer, it is just that C++ allows us to use it like a constant pointer.

```cpp
int a[10];
cout << *(a) << endl;      // a[0]
cout << *(a + 1) << endl;  // a[1]
cout << a + 2 << endl;     // &a[2]
a = &"123";  // no way
```

Function pointers - useful in functional programming, that is, pass a function type as an argument of another function

```cpp
int myFunc(double x) {
    return (x > 0.0 ? 1 : -1);
}
```

Declare a function pointer `fp` with `typedef` (recommended)

```cpp
typedef int (*intDoubleFunction)(double);  // define a type, now intDoubleFunction is a pointer type of a specific function type
intDoubleFunction fp;                      // declare fp, now fp is a concrete function pointer of that pointer type
fp = myFunc;                               // assign a value (a concrete function address) to fp
fp = &myFunc;                              // function names are essentially the same as function addresses
intDoubleFunction fp = myFunc;             // declare and define fp in one line
```

Declare a function pointer `fp` without ```cpp (not recommended)

```cpp
int (*fp)(double);  // this looks concise but it's less straightforward, and the code is not reusable
fp = myFunc;        // if we need to declare many function pointers fp1, fp2, ..., we have to repeat our code many times
```

Use a function pointer

```cpp
fp = myFunc;
fp(0.25);  // equivalent to myFunc(0.25)

int f(int (*fp)(double), int x) {
    return (*fp)(x);  // we can extract fp before making a call
    return fp(x);     // this also works because both (*fp) and fp in essense represent the function address
}

f(someIntDoubleFunction, 10)
```

C style dynamic memory allocation - the return type of `malloc()` is `void*`, so we have to apply explicit type conversion to it before assigning it to other pointers. `malloc()` only allocates space but does not create instances. If we want to create object instances while sticking to the C style `malloc()`, then we must use the placement new operator, the syntax is `new(address) Object()`;

```cpp
int* p = (int*) malloc(sizeof(int));  // explicit type conversion
int* p = new int;  // C++ equivalent

int* p = (int*) malloc(n * sizeof(int));  // explicit type conversion
int* p = new int[n];  // C++ equivalent

free(p);  // free memory
delete p;  // C++ equivalent
delete[] p;  // C++ equivalent

Point* p = (Point*) malloc(sizeof(Point));  // allocate memory space
new(p) Point();  // placement new to create an instance

Point* p = new Point();  // C++ equivalent to the above 2 lines combined
```

C++ style dynamic memory allocation - new and delete must be paired, and vice versa. Never delete twice, never delete without new, otherwise undefined behavior. Memory allocated for a variable is on the stack, it cannot be freed using delete, memory allocated using new is on the heap (free store), and it's the programmer's responsibility to delete it after use in order to prevent memory leaks. For large piece of data, using new to allocate memory can help save memory because dynamic binding at runtime is better than static binding at compile time. The C style malloc can only allocate space, but C++ new can allocate space and create object instances at the same time.

```cpp
int* pt = new int;     // allocate space for an int at runtime, not initialized
int* pt = new int(2);  // initialize with int 2
int* pt = new int();   // initialize with int 0

*pt = 1001;    // store a value there
delete pt;     // free memory (clear data in that address), but pt still points to that address
pt = nullptr;  // reset to NULL pointer

Point* p = new Point(0,0);  // allocate space and create an instance
delete p;

int tacos[10];  // static binding, size fixed at compile time
int* pz = new int[size];  // dynamic binding, size set at run time
delete[] pz;
```

About memory leaks:

A memory leak reduces the performance of the computer by reducing the amount of available memory. When you have memory leaks in your program, the program is effectively using more memory than it really needs to.

A memory leak is simply memory that a process no longer has a reference to, and thus can no longer free. However, the OS still keeps track of all the memory allocated to a process, and will free it when that process terminates. It’s not like that once you have a memory leak, it will not be freed up and reused until you reboot the machine, that’s a common misunderstanding.

Constant pointers and pointer constants

```cpp
// 'const' before '*', this is a constant pointer
int n = 10, m = 100;
const int* p = &n;
int const* p = &n;

// the value of the variable it points to cannot be changed via this pointer
// but ofc it can be changed in other ways, and it can also points to other addresses
*p = 5;  // not allowed
n = 6;   // allowed
p = &m;  // allowed

// 'const' after '*', this is a pointer constant
int* const p = &n;

// we cannot make it point to other addresses, but the value of the variable it points to can be changed via it
*p = 8;  // allowed
p = &m;  // not allowed

const int* const p = &n;  // neither the address nor the value it points to can be changed
n = 999;                  // but of course the value it points to can always be changed in other ways
```


About lambda expressions:

the type of a lambda expression is not fixed, different lambda expressions may have different types

for example, a lambda expr which takes in a double and returns an `int` has the type `std::function<int(double)>`

in the [capture list], we cannot capture global variables, they are always visible and can be modifed in lambda

a lambda expression is essentially a function, but it behaves like a variable, a special type of variable

when we define a function, there's no semicolon `;` at the end: `int f(int) {}`

when we define a lambda expr (variable), there must be a semicolon `;` at the end: `auto f = [](int){};`

if the lambda expr is not definitive, we often use template `U` to refer to its general type, which means [U]nknown

if the lambda expr must be saved, we will explicitly write its type `std::function<T>` (must `#include <functional>`), otherwise we write its type as auto

if a function returns a lambda expr, we can write its return type as `decltype(auto)` (C++14 only), auto asks the compiler to infer the type of a variable/argument for us, `decltype(auto)` asks the compiler to infer the return type of a function for us

Uniform or brace initialization {} - https://stackoverflow.com/questions/24953658/what-are-the-differences-between-c-like-constructor-and-uniform-initialization

```cpp
int arr[] = {1, 2, 3, 4};          // initialize an array
int arr[] {1, 2, 3, 4};            // = is optional
vector<int> v = {1, 2, 3, 4};      // initialize a vector
vector<int> v {1, 2, 3, 4};        // = is optional
Point p[3] {{1,2}, {3,4}, {5,6}};  // initialize an array of 3 points (1,2), (3,4) and (5,6). (nested brace initialization)

vector<int> v(100);  // creates a 100-element vector
vector<int> v{100};  // creates a 1-element vector, holding the value 100.
```

when uniform initialization {} is used with auto, that creates a `std::initializer_list`.

```cpp
auto var = {1, 2};  // creates a std::initializer_list, with var as its identifier
```

C++ input stream

```cpp
while (std::cin >> word) {  // condition is true only if cin stream is valid (no failbit, badbit, eof...)
    ...
}

while (std::cin >> v1 >> v2) {
    ...
}

while (cin >> word, !cin.eof()) {  // comma operator "," returns the rightmost expression as the result
    if (cin.bad()) {
        throw runtime_error("IO stream corrupted");
    }
    if (cin.fail()) {
        cerr << "bad data, try again";
        cin.clear(istream::failbit);
        continue;
    }
    ... // process word
}

istream::iostate old_state = cin.rdstate();  // remember current state of cin
cin.clear();
...  // process input
cin.clear(old_state);  // restore cin to old state

stream.setstate(ifstream::badbit | ifstream::failbit);  // set multiple bits at once using bitwise OR operation |
```

There are 3 ways to flush an output stream

```cpp
std::cout << "Hello " << "world!" << "\n";        // this will NOT flush!
std::cout << "Hello " << "world!" << std::flush;  // flushes the buffer; adds no data
std::cout << "Hello " << "world!" << std::ends;   // inserts a \0, then flushes the buffer
std::cout << "Hello " << "world!" << std::endl;   // inserts a \n, then flushes the buffer

// besides, whenever "cin >> value" executes, cout is automatically flushed
```

How to flush after every `<<` operation (rarely used)

```cpp
cout << std::unitbuf << "1" << " 2" << " 3" << ... << std::nounitbuf;  // is equivalent to
cout << "1" << std::flush << " 2" << std::flush << " 3" << std::flush << ... << std::flush;
```

Basic file streams

```cpp
ifstream input("foo.in");  // create a file stream + open + bind in one line
ofstream output("bar.out");

// file open modes
ofstream outfile("file1");                                   // by default truncates file named "file1"
ofstream outfile("file1", ofstream::out | ofstream::trunc);  // same as above
ofstream outfile("file2", ofstream::app);                    // append mode

fstream file("foobar", fstream::in | fstream::out);  // a fstream file is opened for both read and write (by default)
```

References vs pointers !!!

```cpp
int x = 1024, y = 2048;
int *p1 = &x, *p2 = &y;
p1 = p2;  // now both p1, p2 points to y

int &r1 = x, &r2 = y;
r1 = r2;  // assign y to x, x has changed
```

References do not occupy memory, it’s just a symbol. Under the hood, references are just syntactic sugar around pointers. Pointers however is a real type, they are 8 bytes long on 64-bit systems (or 4 bytes long on 32-bit systems).

```cpp
int* ip[4];    // array of pointers to int
int (*ip)[4];  // pointer to an array of 4 ints, no practical use
```
Confusion about the `static` keyword:

static within a class/struct - only one copy across all class/struct instances, shared memory address

static within a function/file - internal linkage, keeps only one copy of the variable, private to a single source file, not visible to others, not global


Every container has the default ctor without parameters to make an empty container - `container<T> c`;

vector elements are stored in contiguous memory, `insert()` and `erase()` are expensive, accessing elements is fast.

list elements are not stored in contiguous memory, `insert()` and `erase()` are fast, accessing elements is expensive.

deque is double-ended, `insert()` and `erase()` are fast on both ends but slow in the middle, accessing elements is fast.


Classes in C++:

a typedef inside a class is only local to this class, not visible to others.

use initializer's list to initialize members in constructor.

the order that members get initialized is the order that they are declared in the class, not the order that they are given in the initializer's list.

if members' initialized values are dependent on each other, it’s important to declare them in the right order.

`Foo:Foo(): i(10), j(sqrt(i) + 3*i + 999) {}`  - an initializer's list can have any complicated expression.

Pass by references vs pointers: use references whenever you can (preferred), and pointers when you have to.


## Silver Review

`memmove` vs `memcpy` (both are C library functions)

`memcpy` stands for "memory copy." It is used to copy a specified number of bytes from a source memory location to a destination memory location. It doesn't check for overlapping memory regions. If the source and destination regions overlap, the behavior is undefined, and it can lead to unexpected results.

`memmove` stands for "memory move." It is used to copy a specified number of bytes from a source memory location to a destination memory location, even if the source and destination regions overlap. memmove performs additional checks to handle overlapping memory regions. If there's an overlap, it ensures that the copying process is done in a way that preserves the integrity of the data.

Because of the overlap checks and potentially more complex copying logic, `memmove` is slightly slower than `memcpy`. Generally, `memcpy` is faster.



the "M&M Rule", mutable and mutexes (and atomics) go together (https://herbsutter.com/2013/05/24/gotw-6a-const-correctness-part-1-3)



`__forceinline`



RVO, NRVO

- https://en.wikipedia.org/wiki/Copy_elision#RVO



Can I have default arguments in a virtual/override function?

Yes, the C++ Standards allows this, but there are some caveats in the context of inheritance and polymorphism. While you can have default arguments in a virtual/override function, the defaults in the base class are not inherited by derived classes. They are part of a function’s signature, meaning that you can have different default values in the base class vs the derived class.

In terms of which default value will be used - it is determined by the static type of the pointer or reference denoting the object. If you call through a base class object, pointer or reference, the default denoted in the base class is used. Conversely, if you call through a derived class object, pointer or reference, the default denoted in the derived class is used. The takeaway is that, while a virtual function is called on the dynamic type of the object, the default parameter values are always based on the static type. This can lead to unexpected results, for example, what would happen if you call a virtual function that’s overridden in a derived class but you are calling it through a base class pointer? Well, obviously the function in the derived class will be called, but the default value is coming from the base class.

The bottom line is, don’t do that! It’s OK if you want to have default arguments in a virtual/override function, but you need to ensure that the default values match in every class throughout the inheritance hierarchy.

You must never call virtual functions within a constructor.

- https://stackoverflow.com/a/9529188/10677643

What is the default value of a raw pointer?

With smart pointers we don’t have to do explicit initialization as they default to nullptr, but in the case of a raw pointer, it will not be initialized unless a value is assigned to it, otherwise it will just point to some indeterminate garbage address in memory by default. As such, every time we declare a raw pointer (either as a variable or a class member) we must initialize it properly (direct assignment or initialize in your class constructor’s initializer list), some compilers do assign nullptr for raw pointers by default but it’s not a standard feature that we can rely on.

If you fail to initialize a raw pointer correctly, it is essentially the same as a dangling pointer so calling any member function on it could lead to undefined behavior. Using a debugger or memory view, you might see an error message saying that “cannot access the specified memory address” or something similar, often times we will also get a `SIGSEV`, `SIGEMT` or `SIGBUS` in the meantime, after all the address is invalid so it might not even belong to our program's assigned memory space.

Tips: 90% of the time we get a segmentation fault, it’s caused by some uninitialized value!

Sometimes we have a pointer that is not properly initialized (holding an invalid memory address)

Sometimes we have a variable that’s default-constructible but the default constructor fails to initialize all values correctly.

Either way, your program would compile just fine but then segfaults at runtime.

These are the first things to check when you have a `SIGSEV` thrown at runtime.

Speaking of the best practice, we should avoid using raw pointers unless there’s really a need for it. Often times we would use a smart pointer to manage some kind of object or resources, and whatever we do should mostly be done through this smart pointer. In case you are using the `get()` function to retrieve the underlying raw pointer from a smart pointer for the purpose of doing some trivial checks/tasks, remember to store it in a `const T*` variable to ensure const-correctness at all times. Except in some rare circumstances, we would almost never want to call a non-const member function through the raw pointer as that should be done through the smart pointer who truly owns the object.

If the `const T*` variable is a member of a class, make sure to initialize it to nullptr in the constructor as we don’t want to shoot ourselves in the foot when an instance of the class gets instantiated, also don’t forget to check it against nullptr before using it at any point. Above all, keep in mind that its scope safety is not guaranteed so we should only use it within a narrow context. Once the smart pointer gets destroyed, it will become a dangling pointer because it’s still holding the old address value which is no longer valid.



General rule: don’t pass `std::shared_ptr<T>` around, pass the raw pointer instead.

if you pass it by value, reference count will increment

if you pass it by reference, a temporary object needs to be created?

Same thing for `std::unique_ptr<T>`, in general just don’t pass smart pointers around.

`std::endl` is equivalent to `'\n' << std::flush`, that flush can cost you at least 9x overhead in your IO, so avoid using `std::endl` and just use `'\n'` instead.



What is IIFE?

Make sure the obey the Rule of 0

Remember that every time you declare a virtual destructor in your class, you are essentially preventing the compiler from generating the move operations so you lose all the movability. To fix this, add the declaration of them using `= default` in your base class, and derived classes don’t need a virtual destructor because they will inherit the base one by default.



Const methods should be made thread-safe?



It’s not always the best to pass a string as `const std::string&`. If you know it’s going to be totally consumed by your function, you can declare it as passing by value and then move it.

Find a post on stackoverflow on this.

Always prefer `std::array`, then `std::vector`, then only differ you need specific behavior.

Performance wise, `std::array` is the best of all with literally 0 overhead, don’t use expensive containers like `std::list` unless you really have to (for a good reason).


In Python we would use `from functools import partial` to create partial functions.

In C++, we should use lambda functions to achieve that, it has 0 overhead compared to a direct function call. In this case, please avoid `std::function` and never use `std::bind`, these two also work but are 2~3 times slower.

In a performance sensitive function, all data needs to be local to that function, avoid non-local data as much as possible unless you really have a good reason. Note that static data actually has a hidden cost associated, it’s not as fast as local data. Based on the C++11 rules static data must be thread-safe, so it actually needs some kind of mutex protection under the hood and that has an overhead.

If you know that a class or method will be the final version, mark it as such. Proper use of `final` can help the compiler optimize virtual function calls (e.g. make them inline).



General performance tips?

Avoid making unnecessary copies, utilize reference, pointer and move semantics wisely.

Construct in place, placement new, usually not a big deal but can be crucial for complex objects.

Allocate memory on the stack unless you really need the heap for large data size or longer lifespan.

Understand what are commonly slow, e.g. excessive copying, reference counts, dynamic memory allocation, lookups in the vtable, I/O operations, recursion, branching, etc.

Yet more importantly,

Stop doing premature optimization! e.g. `i++` and `++i` makes no difference with `-O3` enabled.

Do not overthink performance in the early development stage, until you really have to optimize.

Most slowness can be solved by using the right data structure or optimizing it, this often leads to over 70% improvement in performance.

Nothing obvious? Try using a profiler to find out the slow part, dissemble it and see what you can do.

Otherwise, you would need to think about your program and make some guesses.

Erase-Remove Idiom in C++

- https://www.geeksforgeeks.org/erase-remove-idiom-in-cpp/
- https://www.codeproject.com/Articles/1227392/Erase-remove-Idiom-Revisited

Another way to do [this](https://stackoverflow.com/a/1038757/10677643), this solution has the upside of being able to do something with the element before removing it, and it works on containers like `std::map` and `std::unordered_map` as well, not just on `std::vector`.

Notice that the expression that is executed after every iteration of the loop and before re-evaluating the condition is marked as `/* BLANK */`, instead, the iterator it is manually modified in all execution paths in the body of the for loop, that’s how it works.

an abstract interface class in C++ always has a `virtual ~dtor() = default`, 但是这个abstract class不需要有ctor（通常没有），只定义一些关键性的method的接口规范。这样derived class就可以自行定义它们想要的ctor构造函数了，没必要在abstract class里去限制ctor的形式。或者一般也可以把ctor放在protected里面，避免这个abstract interface class被直接instantiate，abstract interface class的ctor不需要有参数，直接 `protected: ctor() = default;` 就行了，derived class依然可以去自由的定义自己的ctor，可以有自由的参数形式。

一个C++ class里，对于同一个member你可以有两个同名的accessor，一个返回non-const的一个返回const的，只是return type是否const的差别而已。这样的话，compiler会在不同的callsite自动判断出caller是否有改动该member，没有的话它就会自动去call那个const的版本，避免意外的change。当然你也可以自己explicit写明return type来决定调用哪个版本。

在一个STL容器上做for循环的代码没问题，不过还有很多时候我们更多的是用 `std::transform` `std::copy` `std::remove_if` 之类的各种std的algorithm里面的函数，后期还会用更多ranges library里面的函数。自己写for循环一般都是做比较简单的操作，而用algorithm/ranges里面的函数更适合做各种特定的事情，因为这些函数是被优化过的，很可能比自己写的跑得快。

jemalloc是啥？把它拆开来，就是je + malloc，它是一种malloc的variant，jemalloc is a general purpose malloc implementation that emphasizes fragmentation avoidance and scalable concurrency support. 说白了，它就是malloc用来分配内存的，只不过着重强调了鲁棒性来降低memory fragmentation和concurrency scalability。还记得吗？memory fragmentation在skybox二面的时候被问到过，就是你有2G的可用内存，但它们不是连续的内存地址，那你就没法把它分配给一个2G的std::vector，因为vector要求在内存中必须是adjacent连续的，你分配了就会出现memory fragmentation的错误，这意味着你有100G的内存并不代表你可以随意分配使用这100个G，还要看你的数据结构是什么，假如是linked list，则不存在这个问题，因为链表没法预分配一定量的内存，你加一个节点它才多分配点内存，且它在内存上的存储不是连续的。

不要对代码想当然的做假设然后盲目去找，而是要尽可能多动手实践，无论是什么case情况，什么场景，绝大多数情况下你都至少能确定一到两个地方是代码100%一定会跑到的，那就去那两个地方打断点，等断点停下来了，回头再去看stack trace看代码是怎么被调用过来的。

在C++里想在一个cpp文件中定义internal linkage的private全局变量，可以用`static`关键字也可以用匿名的namespace，但更好的做法是都用，在anonymous namespaces里定义static变量： `namespace { static int x = 1; }`. anonymous namespaces里面还可以定义internal linkage的`typedef`啥的，这些东西都只对当前translation unit可见。

undefined macros are automatically assigned with the value of 0 when used in a preprocessor expression. 就是说，当你用preprocessor表达式 `#if` 去判断一个macro的时候，如果这个宏未定义，则默认它值为0（即false），而不会报错。

怎么去看memory view中的data？假如你现在在 `0x00007f08631c90b0` 这个address这行上，后面跟着的data是 `01 00 00 00 ff ff 2c 2c 8e 8e fd fd 00 00 00 00`，光标闪烁在`01`后面的`00`上，那么该变量的值就是0。读起来很简单，只要知道这里的data是用hexadecimal十六进制表示的就可以了，在十六进制下，每个两位数代表一个byte字节，所以 `ff` 就相当于是二进制的 `11111111` 也就是阿拉伯数字255，所以你会看到IDE帮你每两位空格了一下。四个连续的两位数呢，比如 `01 00 00 00`，也可以代表一个4-byte integer，我们知道标准的int类型就是4个字节32位的integer，大部分POD类型都是4-byte的，所以IDE又帮我们每四个两位数大大的空格了几下。记得，the standard network endianness is actually big-endian，而个人电脑上则是以little-endian为主。但是在读hex number的时候，我们从来不需要去关心endianness，因为我们能看到的hex数字一定都是符合common sense和所有人的习惯来的，左边的那位一定是高位，右边的那位一定是低位，比如11一定是等于`1 * 16 + 1 = 17`，左边的1代表1个16，再比如81一定是等于`8 * 16 + 1 = 129`，左边的8代表8个16，等等。通常IDE还会帮我们把当前变量包含的那些数字都高亮，比如一个long type的变量，会自动高亮它对应的那8个二位数，所以你不用去check变量的类型。在memory view里，可以直接输入一个内存地址然后点View刷新查看，也可以直接输入一个指针，对于普通变量，则需要用&符号来获取它们的地址，比如你可以输入`&foo`来查看foo变量的内存，然而要注意，很多时候我们面对的是一个类和对象里的成员变量，那么必须要加上`this`，把scope写清楚，比如你可以通过 `&this->m_displayFilter` 来访问 `m_displayFilter` 成员变量的内存，但你不能直接输入 `m_displayFilter` 或者 `&m_displayFilter`，假如成员变量是个pointer，那就用 `this->m_myPointer`。

写C++的时候永远要注意，当你要使用一个从smart pointer所get到的raw pointer时，raw pointer的type必须要为 `const T*`，必须带const才能保证const-correctness，而且要注意你只能在附近的很narrow的上下文中去使用这个raw pointer，否则的话很可能原来的smart pointer已经被destroyed了，你没法确保这个raw pointer是不是dangling的。你可以用这个raw指针做一些简单的check什么的，但不要用它去调用non-const的方法，这也是为什么我们要带上const。调用non-const方法会改变它所指向的object的数据，这件事显然应该通过原来的smart pointer去做，毕竟smart pointer才掌管着ownership，否则的话你的程序就乱了，也根本失去了使用智能指针的意义。

下次再遇到segmentation fault，记住了，90%的情况都是由于uinitialized value所导致的，发生段错误，你首先需要去检查的就是，看有没有哪个相关的指针没有在ctor里正确的初始化值，或者哪个class的ctor漏了一些初始化。其次再看下是不是因为python bindings和C++代码不匹配导致memory space无法被正确的map过去。这两个检查基本上都搞定90%的段错误。

```cpp
static_assert(std::is_trivially_destructible<T>::value, "T must be trivially destructible.");
```

In C++, a type is considered "trivially destructible" if its destructor is trivial, meaning it doesn't have to perform any special cleanup or deallocation of resources. A type is considered trivially destructible if it’s:

A built-in type like int, char, or a pointer type.

A struct or class with no user-defined destructor and no non-static data members with non-trivial destructors. (if the struct/class has a non-static member that is not trivially destructible, there’s no way the the struct/class itself can be trivially destructible).

A class that has a user-defined destructor, but the destructor is explicitly defined as trivial using the `= default` syntax in C++11 or later. For example: `struct X { ~X() = default; };`

In particular, a class with a base class that has a virtual destructor is not considered trivially destructible. In C++, when a class has a virtual destructor, it means that it participates in polymorphism and dynamic dispatch (v-table lookups). This results in the compiler generating code to handle the destruction of objects properly, including calling destructors of derived classes through the virtual destructor of the base class, which makes the class non-trivially destructible.

The default constructor can also be explicitly deleted, true of false?

True, deleting the default constructor can be useful when you want to make a class non-instantiable without providing specific data to initialize it, enforcing that instances are constructed with specific parameters.

```cpp
class X {
  public:
    X() = delete;  // deleting the default constructor
    X(int value) {}  // constructor that takes an argument
};

X x;      // This would result in a compilation error
X x(42);  // This is allowed
```

一般我们写 `X() = delete;` 的时候，不只是为了enforcing that instances are constructed with specific parameters。一个更常见的情况是，我们要写一个class，这个class要管理着某些data resources，比如Image class会被用来load an image from disk然后把pixel data保存在class里面，之前我自己写的这个类是用unique_ptr配合一个它的custom deleter来管理的，内存默认是分配在heap上的某个随机区域，但假如你想要更加finer control over memory，你就需要把默认ctor都给delete掉，再创建一个private的构造函数`Image(size_t size, uint32_t width, uint32_t height)`，然后自己写一个`New/Create`函数，这样用户就只能通过这个函数来创建class的实例了。在这个函数里，你可以先算好创建Image的一个实例要多少size的memory，然后在某个你想要的已知地址的内存区域里，手动去分配一块内存，然后再用placement new在指定的地址上去调用那个private的ctor，如此一来你的实例就被创建在指定的内存里面了，于是你就可以用到很多自己的memory tracker工具。


Are these loops equivalent?

```cpp
for (size_t i = 0, size_t n = w * h; i < n; i++)  # first loop
for (size_t i = 0; i < w * h; i++)  # second loop
```

No, although they do both iterate the same number of times, in the second loop, the expression w * h is computed for each iteration of the loop. Most modern compilers can perform an optimization known as “loop invariant code motion”, they can recognize that `w * h` is a constant within the loop and may hoist the calculation out of the loop, effectively computing it only once, but it's not guaranteed, so be cautious.


union in a class

If you have a class member whose type is a union, the intention is most likely that you want to switch between which member is active inside the union. For example, given a class like this:

```cpp
class Base {
public:
    union MyUnion {
        A a;
        B b;
        C c;
    };
};
```

The implication is that we want to derive from the Base class, and each derived class can decide which member in MyUnion (a, b or c?) should be active and used by other member functions.

A Union is just like a struct or class but has many limitations. That said, it still has a ctor and a dtor. If there’s no default constructor for a union, the default constructor for the first member (in our case, `A a`) will be used for the union as a whole. So when the class instantiates, A’s default ctor will be called, and by default a is the active member.

随后当我们再去access其他union里的成员的时候，比如说我们现在access b，那么B的ctor就会被call，把union里的active member切换成b，这样我们就可以随意切换用union里的哪个成员了。

In C++ multithreaded programming, it's important to use fixed-width integer types like `int32_t` to ensure consistent behavior across different platforms.

In C++, references cannot be reassigned to refer to a different object after their initialization. When a reference is initialized, it is bound to the object it references, and this binding cannot be changed throughout its lifetime.

## Sketchpad Review

What is RVO (return value optimization)

Ternary operator has return value optimization (RVO) so it’s not the same as an if-else (which makes copies).

When to create an object on the heap

The object needs to occupy a large piece of memory (so the stack frame might not fit)

The object’s lifespan needs to extend beyond its defining scope or we want to explicitly control it

Placement new

Placement new allows us to construct an object in a pre-allocated memory location. This can be useful in scenarios where we need fine-grained control over memory management or simply want to avoid making copies or moves. The syntax is like `Foo* foo = new(ptr) Foo(args);` where `ptr` points to the pre-allocated memory address where we want the “placement” to take place.

When using the regular new keyword we can both allocate memory and construct objects, in this case there’s no point using placement new again since all we need can be achieved by new. Even if we want to replace objects at that address, it would still make no sense to use placement new instead of the object’s move ctor. In practical examples, ptr is always pointing to a known address on the stack.

```cpp
char buff[sizeof(T)];
T* t = new(buff) T();
t->~T();

Foo foo(0);
Foo* pf = new(&foo) Foo(1);
pf->~Foo();
```

For placement new, the operator in question is operator `new()` rather than operator `new`. These are two different operators, please do not confuse them. While `delete` matches `new` and `delete[]` matches `new[]`, there is no matching operator for operator `new()`, therefore it is required to call the destructor manually when using placement new or any overloaded form of operator `new()`, otherwise data is not cleaned up so we could run into inconsistent states, resource leaks or even undefined behavior.

Bare in mind that operator `new()` is not the same as operator `new`, it’s only used to construct an object in pre-allocated memory but does not allocate memory by itself, memory allocation is done separately. Be aware that if the ctor of the object throws an exception, it's our responsibility to properly clean up the memory and any resources before allowing the exception to propagate further.

When should we use `std::weak_ptr` instead of `std::shared_ptr` nb mn

A weak pointer is just like a shared pointer except that it doesn’t increase the reference count or claims ownership of the underlying object. It is primarily used in situations where we don’t need the ownership. USD uses `TfWeakPtr<T>` quite extensively which serves exactly the same purpose.

Another scenario is where we have lots of shared pointers referencing one another and we do need that shared ownership. But if A refs B which refs C which refs A, we end up introducing circular dependencies. The ref count will never decrement to 0 so there’s no way to release our memory. In this case `std::weak_ptr` and `std::shared_ptr` are often used together to manage circular references.

What is an integral type in C++

In C++, an integral type refers to a data type that can represent whole numbers, both positive and negative, without any fractional or decimal parts. C++ provides several integral types including int, short, long, long long and their unsigned counterparts, plus the two special integral types char and bool. It is also possible to create your own type in C++ that behaves like an integral type. This technique is often referred to as creating a strongly typed enum and it’s used to maintain type safety, but that’s just another topic.







When you want to refer to a null pointer, use `nullptr`, not `0` or `NULL`.

`thread_local`

`dynamic_cast` vs `dynamic_pointer_cast`

functors

cv-qualifiers? `volatile`

`scoped_lock`

`strlen(const char*)`

name mangling or name decoration

```cpp
extern "C" void spiff(int); // use C protocol for name look-up
extern void spoff(int); // use C++ protocol for name look-up
extern "C++" void spaff(int); // use C++ protocol for name look-up
```

__declspec

A functor is any object that can be used with `()` in the manner of a function. This includes normal function names, pointers to functions, and class objects for which the `()` operator is overloaded.

- A generator is a functor that can be called with no arguments.
- A unary function is a functor that can be called with one argument.
- A binary function is a functor that can be called with two arguments.

- A unary function that returns a bool value is a predicate.
- A binary function that returns a bool value is a binary predicate.

Functors vs lambda expressions? lambda cannot be passed around

when to use `std::initializer_list<T>`?

throw exceptions

File I/O

Uniform Initialization

the list-initialization syntax can be used in new expressions:

```cpp
int * ar = new int [4] {2,4,6,7};
```

The syntax also provides protection against narrowing

```cpp
char c1 {1.57e27}; // double-to-char, compile-time error
char c2 = {459585821};// int-to-char,out of range, compile-time error
```

However, conversions to wider types are allowed. Also a conversion to a narrower type is allowed if the value is within the range allowed by the type:

use `decltype` in C++

Trailing Return Type

```cpp
template<typename T, typename U)
auto eff(T t, U u) -> decltype(T*U)
{
...
}
```

`using (alias)` vs `typedef`

The `forward_list` container is a singly linked list that can be traversed in just one direction; it’s simpler and more economical of space than the doubly linked list container.

lvalue vs rvalue Reference

```cpp
using Base::Base;
```

Note that an inherited base-class constructor only initializes base-class members. If you need to initialize derived class members too, you can use the member list initialization syntax instead of inheritance:

```cpp
Derived(int i, int k, double x) : j(i), Base(k,x) {}
```

`std::function`

Variadic Templates

```cpp
template<typename T, typename... Args> // Args is a template parameter pack
void show_list3( T value, Args... args) // args is a function parameter pack
{
...
}
```

void WhenToWriteMoveCtorManually() {
    对于目前我的项目来说，没有一个类需要我手动去写move ctor以及move assignment operator。
    因为所有的资源都是在GPU那边的，我们在C++端没有直接控制权，想修改或更新资源必须通过OpenGL的API。
    所以，我们的所有类当中，所有的成员都是简单类型的，比如GLuint，int，float这种，要么是std::vector. std::map, std::shared_ptr,
    std::unique_ptr等等这种现成的容器和智能指针，而且他们全都自带copy/move的功能实现，所以我们只需要隐式或显式的告诉compiler，帮我
    自动生成默认(=default)，就可以了。随后编译器就会生成默认的copy/move ctor以及assignment operator，根据继承的关系来帮我们自动
    满足rule of five，也就是对个class member依次做copy/move的处理。只需要稍微注意一个小点，就是std::unique_ptr是move-only的，就可以了。

哪怕是utils里面的Image类，我们的类是在管理从stb中读取过来的raw图像数据，是一堆pixels资源，但由于这个资源是用std::unique_ptr来
管理的，我们不用任何心，std::unique_ptr会帮我们管理好，只要custom deleter给它就好了。我们还是不需要手动去写move和copy。

那么，到底什么时候需要我们手动去实现move ctor以及move assignment operator呢？
就只有当我们在直接的管理heap内存的时候，也就是ctor中使用了new操作符分配内存的情况下，才需要。这时候，我们需要保证每个copy或move的
ctor以及赋值符都正确的处理好内存，在哪怕是可能会抛exception的地方也要delete释放资源，如此一来，compiler自动生成的默认版本，也就是
简单的逐成员的copy/move，并不去知道怎么delete，所以就满足不了我们的需求了，要我们手动实现。这个时候，实现请参考copy-and-swap idiom
<https://stackoverflow.com/questions/3279543/what-is-the-copy-and-swap-idiom>
<https://stackoverflow.com/questions/5695548/public-friend-swap-member-function>
<https://mropert.github.io/2019/01/07/copy_swap_20_years/>

不过说到底，现代的C++让我们尽量少自己去手动new，我们的代码中要尽可能避免出现new和delete，所以本来就不太会用到。不确定时可以测试:
static_assert(std::is_nothrow_default_constructible<A>::value, "");
static_assert(std::is_copy_constructible<A>::value, "");
static_assert(std::is_copy_assignable<A>::value, "");
static_assert(std::is_nothrow_move_constructible<A>::value, "");
static_assert(std::is_nothrow_move_assignable<A>::value, "");
static_assert(std::is_nothrow_destructible<A>::value, "");

}

void ImplicitDeclaredSpecialMemberFunctions() {
    在OOP继承当中，如果一个base类定义好了copy/move的ctor和assignment operator，即满足了rule of 5（由于是base类所以还包括一个
    virtualdestructor），那么对于derived类来说，只要新加的data member都是自动可以被copy和move的，而没有用户自定义的不可copy/move
    的类型，那么就不用去显的声明和定义derived类自己的copy/move的ctor和assignment operator，只要保证没有自己写任何的copy/move函数，
    且没有写destructor（不需要写或者base类的virtual destructor就已经足够了），那么编译器会自动帮我们生成，这个叫做Implicitly-declared
    换句话说就是，我们的base类已经满足了ruleof five，然后所有的derived类也不再需要特殊的destructor，那么这个时候，每个derived类，
    就只需要写一个（或多个）普通的constructor就足够了，剩下四个copy/move的ctor和assignment operator，编译器都会帮我们自动生成，
    从而满足rule of 5（base类的virtual destructor当然是肯定会被call的）

另外，考虑一个derived类的move构造函数：
Derived(Derived&& other) noexcept : Base(std::move(other)) {
    derived_member1 = std::swap(other.derived_member1);
    derived_member2 = std::swap(other.derived_member2);
}
为什么other在initializer list中已经被std::move了以后，我们在body里还能去swap derived类新加的成员呢？不是说std::move了之后，
other这个物体失效了吗（处于一个clean null state等待被destruct，但所包含的数据已经无意义了）？这是因为，在继承的这种关系中，当
Base(std::move(other))被执行时候，std::move(other)的类型是Derived&&，而Base类只认识Base，所以它会被隐含的转换成Base&&，
然后base类的move构造函数只会去处理base类有的成员而derived类新加的成员是没有被动过的。

只有当成员比较复杂，或者实在拿不准的时候，我们才需要自己去手写move constructor和move assignment operator。
但是这个时候，我们可以利用copy-and-swap idiom来简化代码的实现。可以参考这里：
<https://stackoverflow.com/questions/3279543/what-is-the-copy-and-swap-idiom>

}

void CppMisc() {
    always use structured bindings when iterating over a map or unordered_map
    // this is bad
    for (const auto& entry : word_histogram) {
        std::cout << entry.first << " : " << entry.second << "\n";
    }
    // this is good
    for (const auto& [word, count] : word_histogram) {
        std::cout << word << " : " << count << "\n";
    }
    // we can also retrieve the pair right after insertion
    auto [iter_where, inserted] = map.insert({key, value});

如何更好的理解右值引用？从概念上解释：
An lvalue reference means that x is an alias of some pre-existing object, whose lifetime and ownership is
managed independently.
An rvalue reference means that x will refer to either a temporary object created by the compiler at the actual
call site, or a pre-existing object that the caller passes with std::move()
所以说，用左值还是右值，不只是语法上的问题，同时也是传达给阅读代码的人，告诉对方我这个参数是从哪儿来的，大概会是用作什么的。

c++ std::map [] is not a const operation，因为[]当key不存在时，会插入新的pair到map中，所以它不是const的。
因此，[]无法在const std::map上使用，也无法在一个类的const方法中使用，否则会编译不过，出现C2678 no operator found...的错误。

ternary operator ?: is different from if-else, it won't do any branching!!!
C++20开始，有了likely unlikely关键字提示给编译器，我们就可以把if-else branching优化到和ternary运算符一样快了。

如果代码显式的定义了任意一种ctor或者dtor，哪怕body是空的，编译器也会认为它是non-trivial的。
只有编译器自己implicit生成的，或者是代码显式的使用了implicit指令=default或=delete的情况下，才被认为是trivial的。
trivial与否的区别就在于，在trivial的情况下，编译器会做优化，速度快很多，而non-trivial则会慢一些

virtual inheritance是专门用来处理菱形的dreaded diamond multiple继承的，通常用不到，可参考stackoverflow我的bookmark

std::tuple是一个加强版的std::pair，它不是一个STL标准容器，它是用来存放多个不同类型的object的一个数据结构。
std::tuple主要的用法是，用于让一个函数一次性的返回多个值。它会自动建立一个临时的struct来包含所有成员，这样我们就不用自己定义struct了。
auto& [a, b, c] = std::tuple(1, 3.14f, "hello");
std::cout << a << std::endl;
std::cout << b << std::endl;
std::cout << c << std::endl;
这个是C++17 引入的structured binding功能，方便用于让一个函数返回多个值。
相比于自己定义struct并返回该struct，这样代码更干净，并且std::tuple的构造函数析构函数会自动处理好。如果要手动访问tuple中的某个元素时，
可以使用std::get<I>，但是I必须是compile-time constant。并且因为tuple不是STL容器，我们无法循环遍历它（而且元素类型还不同）。
可以看到，std::variant其实就是在tuple的基础上建立的。通常只有在函数返回多个值时，会用到std::tuple，它会自动试图去调用move，避免copy。
c++17开始，构造函数自带argument deduction，所以再也不需要用std::make_tuple了，std::make_tuple没什么用，直接std::tuple()即可。

smart pointer一般都是按照value返回的，return by value，其实不需要担心这样会导致shared_ptr的use count不断的++和--，因为编译器会
做一个叫做RVO(return value optimization)的优化，实际上并不会有大量的copy和性能损耗。

关于move semantics，这次彻底要理解对！
不要把std::move()理解成一个function，理解成一个static_cast<T&&>才对。它只是做一个lvalue到xvalue的转换(rvalue的具体一种)，而且
是在compile time做的，和runtime没有一点关系。我们知道，std::move()是为了避免copy存在的，所以不会copy，除非是primitive的类型比如
int float，那么move和copy没有区别（基础类型只能copy）。更重要的是要意识到，std::move(x)只是返回一个由x指向的右值，它并不会去销毁x
std::move(x)结束之后，x原来的值被关联给了等式左边的变量，data的值被move了，但是原来的x这个变量或对象依然存在，存储空间依然存在，只是
里面的值被掉包了而已：std::move() does not actually move anything，think of it as rewiring data to a new storage and
invalidating the old data, but the old storage is still there.

简单一点，我们可以把右值理解为一个常量或中间值的数据，它在CPU中是没有存储空间的，不占据空间，只是一个值，为了让这个值有意义，那么它接下
来很快要被赋予给一个左值的变量，依赖于左值的内存空间，数据的值才得以存续。
a = std::move(b)的意思是，b本来有一根线（可以想象成指针）指向某个数据x，这个数据x是依赖于b变量的存储空间而存在的，一开始，x只有和b的
这一条连线。随后，std::move(b)找到了这跟连线，并把这跟连线赋给了变量a，于是，x现在就分别和a/b有一条连线了。

对于class的move ctor和move assignment operator而言，我们站在move ctor的body里这个角度看，是会看到一个叫做other的物体，准备要
和我们现在身处的这个物体交换数据。也就是说，other代表的是move-from的物体(source)，我们所在的这个物体是move-to的物体(target)，交换
结束之后，我们拿到了other原有的数据。然而这里非常容易理解错。
事实上，这里的交换，只是概念上的交换，具体是不是真的交换，取决于我们的move ctor做了什么。

[1] 假如我们自己手写move ctor，我们通常先把自己所在的物体的数据清理干净，成为一个hollow物体，也就是达到一个clean null state，然后
我们会逐成员的去用std::swap()函数与other的对应成员交换数据，这才是真的交换。之所以把数据先清理成一个clean null state，是因为这些数
据要兑换给other，而other随后马上会被destruct掉，只有保证数据是干净的初始state，other在被destruct的时候才不会出错，误删资源什么的。
————这是真正的交换，即swap。

[2] 假如我们没有手写，而是用了=default这种显式的方式让编译器自动为我们生成move ctor（或者隐式的生成也一样），这时候，自动生成的move
ctor并不会先把数据清理成初始值再去swap什么的，它很蠢，它只会逐成员的去调用每个成员的move ctor，也就是说，我们所在的这个物体将会得到一
根新的连线，由这跟连线把当前物体和other所对应的数据连起来，但other和这堆数据的连线还在。至于other的成员的值是否有发生改变，就要分情况
讨论了，如果是int float这种成员，move相当于是copy，所以other的该成员的值没有变，并没有任何物理意义上的move或者swap发生，而如果是
std::string成员或者是我们自定义的一个实现了swap-move的类型T，对该成员调用move ctor是会发生实质上的swap交换的，那么other的该成员的
值就会变成当前物体的同成员的当前值。接下来呢，所有成员的move操作都结束了，other会被destruct掉，等于说是，other和那堆数据的连线就会被
剪断了，只留下我们当前物体和数据的一根连线。由于在剪断的过程中，other的数据并不一定会是一个clean null state（有些可能是被copy了），
如果析构函数里面做了任何会invalidate那堆数据的操作，那我们留下的这个连线，就是dangling的，连线连到的是一堆已经失效的数据。由此可见，
当我们在管理resource的时候，常常并不能依赖于compiler自动生成的move ctor，它达不到我们想要的效果，必须手动实现。只有当destructor和
那堆数据无关的情况下，才可以用=default，也就是destructor call不会导致那堆右值的数据invalidated。举个例子，比如说class只有几个
float和int的成员，每个成员都只包含纯粹的数据，没有任何file handle什么的，还包括几个我们自定义的类型T，但这几个T本来就已经可以正确的
move-construct的。

[3] 在OOP继承的结构中，为了方便干净的管理资源，通常我们会有一个base类声明所有这些资源相关的成员，然后手动的设置好move ctor。接下来，
每个derived的类就不用再重复设置了，如果derived类要定义自己的dtor，那么编译器无法帮我们自动生成move ctor，我们就要自己explicit的
用=default来告诉编译器生成，从而满足rule of 5，如果derived类只有一个普通的ctor，那么我们就什么都不用写，编译器会自动生成rule of
five，这样每个derived类的代码就很干净，以上两种无论哪种情况，derived类的move ctor都会自动去调用base类写好的那个move ctor，base
类的成员是一定会被正确的move的。然而，需要注意的是，假如我们的derived类又有一些特殊的代码逻辑，需要手动去写move ctor的时候，base类
的move ctor是不会被自动调用的，我们的derived类的move ctor的初始化列表里，必须手动写上 : Base(std::move(other))才行。不过一般
当你发现这种情况的时候，通常说明你的base类不够用，可以再去包一层，定义另一个base类：
class Base2 : public Base { ... };
为了代码干净简洁，我们要尽可能的把这些move ctor的mess，都放到一个或几个base类里，让这些base类实现rule of 5，然后上层的每个
derived类里，就要尽量去follow rule of 0，即只定义一个普通的ctor。

<https://stackoverflow.com/questions/70917504/what-does-explicitly-defaulted-move-constructor-do>

使用std::vector时，不仅需要注意construct in place来减少copying，同时还要非常小心dynamic resizing and allocation。
当你知道你的vector有多大的时候，一定要养成习惯使用vector.reserve(n)，这样vector一开始就会准备好n个元素的存储空间，那么接下来的
emplace_back()就不需要每次去resize了。注意reserve和resize是不同的，resize不仅是分配存储空间，而且还会直接construct那么多的
元素，这也要求每个元素的类型必须是default constructible的，resize的作用和vector的构造函数是一样的，相当于是我们显式的调用了
std::vector vec(n)，这在一开始就会把vec填满n个元素，而reserve只是分配足够的存储空间而已，增加了vector的capacity，而不是size。

有时候我们用vector(n)这个构造函数的形式来预分配存储空间，并同时初始化元素值。这比reserve要多了一个初始化的overhead，
但是接下来，我们可以用vector.at(i)=的形式去填入值，这样减少了push_back()或emplace_back()的overhead。
还有的时候，就是在debug当中，有时我们会故意不去reserve也不用构造函数，故意让vector动态的resize，看代码会不会有脆弱的地方和bug。
这样做主要是为了测试vector<T>所容纳的类型T对不对，尤其是当class T管理资源的时候，看RAII做没做对，move ctor有没有漏东西等等。

此外，emplace_back 从C++17开始，在你emplace了一个元素了以后，还会直接返回你最新的这个元素的引用，方便你做事情，比如：
auto& element = vec.emplace_back(args...);
std::cout << element << std::endl;

然后你需要非常小心，假如你有多个auto& element = vec.emplace_back(args...)的语句，必须保证在这个过程中vector没有重新动态
resize或分配空间。假如动态resize了，你之前的那些element的引用就会变得无效，被invalidate了，他们引用的东西是void，因为那些位置
本来在的元素现在都已经被move到新分配的存储空间去了，搬家了，这时你一定不能通过这个引用去做任何事情。
综上所述，使用vector的时候需要额外小心，无论是为了减少出错，还是为了performance，只要使用了vector，最好永远预先reserve。

// construct in place without copying
std::vector<T> vec;
vec.emplace_back(args...);
std::map<Tk, Tv> map;
map.try_emplace(key, args...)

// 当你使用STL容器来construct in place的时候，一定要注意一个很恶心的bug，无论是emplace_back
// 还是try_emplace，都并不总是真正意义上的construct in place，有的时候还是会进行std::move()
// 操作的，比如当容器需要自动resize或者allocate的时候（所以我们才说是“Amortized O(1)”的时间）
// 就会去move，所以你也要当成是move来看。好几次的错误都是，我在class里新增了一个成员，没有设置
// 默认值，而是放在构造函数里去设置初始值的，但并不是默认值，然后呢，try_emplace的时候被隐藏的
// move了，也就是我实际以为的对象和一个空的默认对象进行swap，然而那个空的默认对象的那个成员，要么
// 值是脏的也就是未初始化的垃圾值，要么是默认构造函数给它的非默认的值，一move，这个成员field就会
// 导致其他依赖于它的代码的bug。所以，一定要记得，要么要主动设好默认值，别只声明，要么每次新加一个
// 成员的时候，保证一定会在move constructor和move操作符里去处理这个值。这个真的很容易忘记，新加
// 成员的时候总是会忘记在move constructor里也一起加一下……

[[nodiscard]]  //代表一个函数的返回值不能被discard，必须要被用到
[[nodiscard]] int Add(int x) { return x + 1; }

auto it = vec.begin();
it++;  // 对迭代器直接加减只适合vector等random access容器，不适用所有容器
std::advance(it, 2);  // 养成好习惯，尽量用std::advance等几个方法
std::advance(it, -2);  // backwards advance
auto next1 = std::next(it);
auto previous2 = std::prev(it, 2);

std::map内部结构是BST，是有序的，所以如果要用自定义object作为key的话，还要override operator< 或者提供一个compare函数。
std::unordered_map是无序的hash table，所以如果要用自定义object作为key的话，要override operator==并提供hash函数。
通常人们喜欢用std::map，是因为它更稳定，速度永远是O(logn)，不存在worst/best case，并且免费的提供排序，同时，std::map比
较轻量级，内存消耗小。除我们要存储成千上万的大量的pair数据，一般都用std::map更好，数据量不多的情况下用std::unordered_map反而是浪费。

}

void Pitfalls() {
    (vcruntime140d.dll) 0xc0000005: access violation writing location 0x00000000.
    这是在使用visual studio的时候，反复会遇到的一个经典错误，有时候不是vcruntime140d，也可能是mtdll等其他dll文件报错。
    这个问题极其难查和浪费时间，以后记住了，这是visual studio的一个bug，不是我们自己代码的bug！！！！！！！！
    症状表现为：之前的代码一直跑的好好的，突然间就报错access violation，比如很简单的copy一个string，两边都有值，结果到了std的
    <string>源文件里，就莫名其妙变成了null pointer，或者某些值显示unable to read memory locations。再比如说，本来代码一切
    运行正常，结果我就加了一个int a = 1的语句，或者新定义了一个const vector，突然间，某些shared_ptr的copy就报错access
    violation了，出现了各种空指针。

原因分析：当出现以上症状时，回想一下，你前面是不是刚刚刷新过premake或者cmake的build脚本？比如，通常当我们重新用premake
build了整个vs的solution之后，回到visual studio中时，vs会马上弹出一个对话框，告诉你solution和project settings已经被修改，
是否reload。然而有的时候，明明premake更新过了，回到vs之后却没有弹出这个对话框，而我们也没有注意到，或者是我们不小心点了cancel，
这样一来就会导致，我们当前正在做的project，和vs所认为的project之间出现了分歧，明明project settings已经更新了，vs也是以新的
settings为标准去debug和运行什么的，但实际上我们的项目还在用老的设置。所以当你继续运行时，一开始正常不会出错，但只要你加了一点点
新的代码，两边就彻底分歧了，可能你只是新声明了一个int，但vs根据新的project settings，build的时候可能会把这行代码编译到其他的
内存区域去，于是就产生了这个巨恶心的问题，难以查原因。
其他原因：除此之外，还有个常见的原因会导致这个问题，就是debug/release版本以及win32/x64版本的不匹配，就是你用debug的project
settings去跑release build，或者反过来也是如此，不过一般这个比较罕见。比较大概率的可能是，某些assertion的用法不对。因为
ASSERT是只会在debug build里面跑的，到了release build，一切ASSERT都不会跑，因为根本不会被编译到release版本中去，所以说，
假如你不小心在ASSERT中做了一些事情，比如malloc分配了内存，而到了release的时候，assert被跳过了于是该内存没有被malloc分配，
那么接下来的代码就会无法读取这块内存。这种情况下正确的做法是throw exception，而不是ASSERT，回忆一下assertion和exception的区别。

在我们的rendererInput结构体rdr_in当中，有个material id的field，这个一般是只用于assimp加载的外部模型的，对于同一模型中的
不同mesh，可以用这个变量来加以区分，采用不同的着色。如果不是加载的模型，而是我们自己的primitive mesh，这个变量是不需要的，也
没有意义，但是要注意，虽然不用，也必须设置为0，否则的话，它就会沿用上一次更新的值，假如上一个画的正好是个model，那这个primitive
mesh就会被误判为是model，从而shader的逻辑会错掉。设置为0是安全的，因为加载的外部模型的material id永远不可能为0. 这是因为，
material id取的是某个mesh的VAO对应的object handle id，当我们加载模型时，0肯定早就被其他的OpenGL object用掉了。

using declarations should only be used after all includes in a .cpp file

OpenGL的完整pipeline流程，必须要熟悉：
<https://www.khronos.org/opengl/wiki/Rendering_Pipeline_Overview>

once we save a shader program to disk as a binary file, it becomes permanent and can be loaded into OpenGL
again. It should be noted that only the compiled data gets saved into the binary, but not the program object
id, so it is a piece of data not owned by any shader program. Later when we load it into OpenGL, we still
need to create a shader program to which the binary data should be assigned. This essentially means that a
pre-compiled shader binary can be loaded by multiple entities, it can be shared by any number of shader
programs (each has a different id) with no conflicts.
Also, data inside the saved binary is implementation dependent, each platform and driver has a different way
of handling it. Therefore, if you try to load a shader binary saved by another platform, the operation is
going to fail with an empty error message. Even if you are using the same driver but of different versions,
it is still likely to break.

normal map和bump map不是一回事。bump map是通过grayscale修改每个像素是偏黑还是偏白，提供像素的depth的错觉，但只有上下两个
方向，它产生的detail是假的，通过旋转camera到不同的角度，就很容易发现，所以bump map只适合模拟大概的细节，优点是比较容易制作。
而normal map其实是新一代更先进的bump map，虽然normal map产生的depth细节也是假的，但它用的是RGB信息来对应3D空间的XYZ，给每
个点都提供了normal的数据，参与shading的计算，所以哪怕camera换了角度也不会失真。

// in spdlog, curly brace '{' needs to be escaped by using '{{'

JPG只有RGB，没有alpha通道，能代表的色彩比较有限，没有透明度，并且压缩是lossy的，所以文件大小比较小，轻便不占内存，但是如果在
网络上传输的次数多了，经过了多次的压缩和解压，图片质量会大幅下降。PNG可以支持最大48bit的色彩，而且有alpha通道，所以色彩空间更丰
富，它的压缩是lossless的，无论怎么传输都能保留原图的质量，但是文件大小一般比较大，不是那么轻便。TIFF格式是一个图片的container，
可以存储多幅图片，文件比较大，可压缩或不压，通常是用来网络传输时打包的。

remember that camera.position and direction is vec4 whose w component has junk, we only use .xyz
this is because our UBO SSBO do not allow vec3 types

ImGuizmo假定一次只能画一个gizmo，通常来说，我们也确实是应该一次只操作一个gizmo，当前被选中的物体的gizmo。
不过对于画gizmo是没有限制的，我们可以一次性同时画多个物体的gizmo，只不过这会导致一个问题，就是ImGuizmo无法判断哪个物体是被选中
的，或者根本就没有选中状态。此时，当我们去manipulate其中一个gizmo的时候，其他物体的transform矩阵也会发生变化，也就是多个物体
之间存在纠缠现象，改动一个gizmo会影响到其他。

about GLuint id = 0 for OpenGL objects:
<https://www.khronos.org/opengl/wiki/OpenGL_Object#Object_zero>

Intel显卡上compute shader不会hang，可以正常运行，但它似乎有个问题是，驱动会自动做一些fbo的后台操作，导致即使你没有进行
glBindFramebuffer的操作，即使你一直在默认的framebuffer上，每个glDrawXXX调用都会触发debugMessageCallback，显示redundant
state change（FBO 0 is already bound）这样的low级别performance通知信息。并不是我的代码的问题，是intel显卡。

AMD显卡上，没有redundant state change的问题，但它非常严重的问题在于driver timeout，总是会莫名的timeout，这也导致它一旦遇到
计算量稍大的compute shader，它就reset不动了。在Intel和Nvidia显卡上都没有这个问题。

终于搞定了这两个bug……以后记住，debug要用RenderDoc这样的第三方工具，在API inspector里一步步看，不仅可以浏览texture，还可以
看到VAO,VBO,IBO的具体信息，看到你绑的shader对不对，源代码是什么。“No Resource”不是出错，而是代表0，就是unbind一个资源。对于
很恶心的bug，重点关注pipeline state中的rasterizer当前state信息，如果是clip不对，或者cullmode不对，或者depth有问题，是非常
难查的，但是这个面板就很有帮助。

当你看到buffer object的id在切换场景之后，不断递增，没有重置，肯定是你哪里没有delete清理干净。我的shader program id不断
增加，是因为我有时候create shader却提前return了，没有来得及delete掉，这就和memory leak的那个bug一样特别容易出错。你以为你
delete或者free了，但可能某个分支提前触发返回了，根本来不及跑到那里，内存就泄露了！！！

还记得那个黑球的问题嘛？？？记下这个教训。
如果你发现某个本来应该很耗时的draw call瞬间完成了，并不代表shader没有被执行。你试着把shader改成就输出一个粉色，结果出来的还是
黑色，这不是因为shader没有被执行，而是因为face culling的原因，导致opengl发现你这个face需要被cull掉，所以fragment shader
一进去就把所有的fragments自动discard掉了！！！！！
当我们draw一个skybox时，或者要计算irradiance map时，记住，只要是render到一个cubemap上的，用draw cube的方式，都必须要先把
winding order反过来！！！！否则会被cull掉！！！
要么SetFrontFace为CW，要么disable face culling。如果shader瞬间返回，一定是因为这个原因，这是draw cube时的一个大坑。
draw cube还有一个大坑就是，如果计算irradiance map这种比较耗时的任务，每个face还来不及执行完，你就切换到下一个face，会导致
GPU的command queue超负荷！！！可能会有CPU和GPU之间的同步问题，然后就会导致，某个glXXXX函数突然就hang住了，永远不返回。出现
这种情况，不是那个gl函数的问题，有时候会卡在glTexSubImage上，有时候会卡在glClear或者glSwapBuffer上，都有可能的。这种时候，
你必须要在画每个face之后，手动去同步，要么用glFinish，要么用glFenceSync这样的sync object。如果是compute shader的话，
那么就一定要glMemoryBarrier。

对于在premake中设定了的macro宏，我们在代码中运用时，尽量不要用#ifdef污染代码格式，而是要尽量把宏转化为C++17的inline
constexpr变量，然后在代码中用if constexpr去访问，可以参考pch.h中对于_DEBUG和__FREEGLUT__的处理。
只不过，我们还可以更进一步，当我们直接想在代码中预定义几个常量时，也不要去自己定义宏，而是全部使用constexpr auto来代替。
如果只是需要在一个cpp文件内部使用，就用constexpr auto就可以了，不需要inline，如果是定义在header里为了想让多个cpp文件都能
使用，那么再用inline constexpr。inline的作用是可以让我们绕开ODR(One Definition Rule)的规则，使得该变量哪怕出现在多个
cpp文件中（即多个translation unit中），也不会相互冲突，前提是这些变量的值必须完全相等。

Parallax Occlusion Mapping (POM) is Not suitable for non-quad surface (e.g. spheres)
It's COMPLETELY unnessecary to clear the contents of an stl container in a constructor.
It's unnessecary to clear the contents of an stl container in a destructor UNLESS the container contains
a pointer or the order of destruction matters. If the pointer has been created using new, it still needs
to be deleted first.

Image access (ILS) ignores all sampling parameters，我们只能按整数的index去访问image里面的值，不能有任何超界的
或者是小数点像素的值访问。使用ILS的时候，一般我们都会用restrict这个memory qualifier，这样GLSL可以做一些优化，速度更快。
restrict是说，只能通过这一个变量来对ILS进行操作，假如这个ILS同时被bind到了多个image unit的话（也就是对应着多个变量），
其他unit的变量是无法操纵它的。一般我们都不要把一个ILS的texture绑到多个image unit上面……

如果你的fragment shader有多个out变量，你要保证每个变量都有被写入值，保证每个分支都会写入每个out变量，哪怕是0也好，否则
值是undefined，特别难debug

bloom不适用于太小的物体，否则每帧需要blur的像素会急剧变化，所以会闪烁的，这个是bloom本身的问题。bloom的物体必须要稍微大一些。
有时候闪烁也和抗锯齿算法有关，同样是后处理的步骤，但如果AA算法在Bloom之前，Bloom就很难找准像素了。要么是bloom阈值设的太低了，
也比较难找像素。
AA和小物体加在一起的话，闪烁就更明显了，因为Blur pass太难精准的判定像素了，每帧被blur的像素都在变化。

如果你的fragment shader有多个out变量，你要保证每个变量都有被写入值，哪怕你只写一个，另一个也会被影响，Any fragment color
values not written by the FS will have undefined values。如果用一个framebuffer的两个texture来做two-pass Gaussian
blur的ping pong，每次你读其中一个texture，写入另一个texture，因为读的那个不能动，所以只能写入一个out变量，这样就是错误的有
问题的。正确的做法是，你的fbo只能用一个render target，对应的只有一个out变量，然后每次ping或者pong的时候，
用`glDrawBuffers()`去切换写入的texture。

当你使用了perspective projection的时候，你会发现场景中边缘物体会有些distorted，比如一个cube在边缘，横边会比竖边长很多，
这个不是bug，是正常的，同时和你的相机fov有关，现实世界里其实也是一样的，你从不同的角度拍照，有不同的projection matrix，
有时候能显腿长，有时候能显脸大，所以你要去找角度。

}

void Std140Std430() {
    GPU驱动的实现是比较复杂的，我们使用的图形API背后，有大量的分布式并行算法，比如著名的prefix sum算法。
    为什么要有std140,std430这样的layout限制，因为GPU是并行结构的，memory必须满足它的并行结构才能运作和加速。熟悉了GPU的内部原理
    结构之后，这个问题就很容易理解了。对于std140的UBO来说，每个非array的uniform的aligned offset和size我们都已经了解了，而如果
    某个uniform成员是array，在不考虑double精度的情况下，无论该array的member是scalar还是vector，the alignment will always
    be rounded up to the base alignment of a vec4。比如说，无论这个uniform是int[]还是uint[]还是float[]还是bool[]，每个
    element都会占据vec4也就是16字节的长度，也就是说真正的数据是在每个vec4长度的x的位置，后面的yzw都是padding。再比如说，无论这个
    uniform是vec3[]还是ivec2[]还是ivec3[]还是vec4[]，每个element也还是会占据vec4=16字节的长度，于是vec3的真正数据是在每个
    vec4长度的xyz的位置，而w是padding。通常，我们永远都不会需要用到double精度的类型，那么可以安全的认为，只要是array，每个array
    element都一定是vec4的长度，也就是4N=16字节。假如有double精度，每个array element的长度可能更大，比如dvec3会被pad到dvec4的
    长度，也就是8N=32字节。

SSBO既可以用std140，也可以用std430。一般之所以用std430，是因为SSBO存储的数据非常大，要尽量避免padding浪费掉的内存空间。
std430相对于140的主要区别就在于，对于SSBO中的某个array成员，当它的类型是scalar或者vector的时候，每个array element并不会被
padded到vec4=16字节的长度。这里的array element并不是没有任何padding，只是padding更少更节约，所以std430的SSBO相对于
std140而言，数据在内存中are more tightly packed。比如说，如果一个变量是float[]，或者是int[]，uint[]，那么每个array
element的长度就是N=4字节，没有padding。如果是vec2[]，则是2N=8字节，如果是vec4[]，则是4N=16字节。但如果是vec3[]的话，每个
array element会被padded到vec4，也就是4N=16字节的长度，所以真正的vec3数据是在每个vec4长度的xyz的位置。一个比较好的习惯是，
永远不要去使用任何3的类型，比如ivec3，vec3或者mat3，而是要么使用vec2，要么使用vec4，这样做不仅是为了避免考虑padding的麻烦，
减少程序bug，同时也可以达到提速的效果，如果你使用了vec4来替代vec3，那么hardware就不用去额外添加处理padding，所以vec4要比
vec3的速度快很多！

在使用UBO和SSBO时，最好的做法是，假装所有的3-element类型都不存在，也就是说，永远不要使用vec3，ivec3，uvec3，mat3，imat3
这样的类型。我们要么使用bool，uint，float这样的scalar，要么使用2-element和4-element的vec以及mat，这样可以消除许多麻烦。
比如说，If you want arrays of vec3s, then make them arrays of vec4s。再比如说，If you want a vec3 + a float，
并且还想尽可能的节省空间，那你就手动的去pack数据，把它们挤在一个vec4变量里，然后用xyz成员去访问vec3的数据，用w成员去访问float的数据。

另外，永远不要在UBO和SSBO中使用自定义的struct类型，不仅很难做对，而且未来升级到SPIR-V和Vulkan的时候很可能会有麻烦。比如SSBO，
假如你需要传一个struct的数据，不要去定义一个包含struct[]的SSBO，而是把struct拆开来，每个struct的成员单独放在一个SSBO
的比如float[]当中，用多个SSBO来处理。

在GPU编程中，注意memory layout始终都是非常重要的，始终要有这样一个概念，大概明白数据在GPU中是如何存储的。
未来主流的GPU architectures在往新的趋势转型，GPUs made today are all single scalar architectures with the
design emphased on strong superscalar vectorization，所以未来比较新的Graphics API当中，可能会有些变化，但目前
来说我们通常还是认为，GPUs typically work with vectorized type

}

void Blending() {
    https://www.andersriggelsen.dk/glblendfunc.php
    glBlendEquation
    glBlendEquationi
    glBlendFuncSeparate
    glBlendFuncSeparatei
    glBlendFunc
    glBlendFunci
    glBlendColor
}

void BufferObjects() {
    UBOs are up to 16KB in size, while SSBOs are up to 128MB or even larger
    UBOs are faster, SSBOs are slower
    shaders do not have write access to UBOs, UBOs are set by C++ application and readonly in the shader
    however, shaders can write to SSBOs directly in GLSL, depending on if writeonly or readonly is used.

UBO和SSBO都属于indexed buffer，它们是一个buffer，同时在GLSL和OpenGL的状态机中，有一个唯一识别的index（即binding point）。
关于它们的binding操作，是通过两个bind函数来实现的：glBindBuffer()以及glBindBufferBase()，或者也可以用glBindBufferRange()
来只绑定一部分的data，但我们并不需要，只要前两个函数就好了。然而它们比较容易被混淆，这里澄清一下。

以UBO为例，对于glBindBuffer() and glBindBufferBase()，我们都需要指定 GL_UNIFORM_BUFFER 为target，但两者并不重复，它们
完全是用于不同的purposes，适用于不同的context。glBindBuffer()说的是把当前的UBO绑定到OpenGL的可写内存区中，这样我们接下来就
可以用glBufferData(),glBufferSubData()或者是对应的DSA版本glNamedBufferSubData()去修改这个UBO的数据了，也就是写入数据到
UBO中，并且让这份数据被upload到GPU。然而，这样做只是更新了UBO的数据，我们还无法在GLSL中去read访问它。By contrast，
glBindBufferBase()说的是，我并不关心这个UBO有没有数据，有什么data，也不会去动它，我只管把它和某个binding point关联在一起，
让用户可以在GLSL中，通过reference定义在这个binding point的uniform block来访问它的数据，并在shader的main()函数中使用这些数据。

所以说，glBindBuffer()只是绑定UBO用于更新data，而glBindBufferBase()是把这个UBO关联到GLSL中某个binding point的uniform
block让人可以访问。所以两者都是必须的，哪个都不能省略（除非用DSA）。glBindBufferRange()也类似，只是把这个UBO中的一部分data关联
到某个binding point。同样的规则也适用于SSBO和TFB，可以参考官方说明：
<https://www.khronos.org/opengl/wiki/Buffer_Object#Binding_indexed_targets>

关于glBindBuffer() and glBindBufferBase()的区别，某些人还会提到block index的概念，比如这个解释：
<https://stackoverflow.com/questions/54955186/difference-between-glbindbuffer-and-glbindbufferbase>
参考link中的figure图表，我们可以发现，block indices只不过是uniform blocks在某个具体的shader中的下标索引，也就是描述一个
uniform block在某个给定的shader中是第几个被声明的block，就和一个元素在数组中的下标一样，完全取决于你在shader里怎么按顺序声明的。
对于我们来说，我们使用的每个uniform block，都一定会显式地指定它的binding point，所以其实我们并不需要block index这个概念，
不用管。假如我们没有显式的去specify layout(binding=xxx)，那么才会需要去查询一个个block的block index，再去查询该block
index对应的binding point。而我们已经自己定义了binding point，就不需要任何查询了。

在使用DSA的情况下，UBO和SSBO这样的indexed buffer，是完全不需要glBindBuffer()的，因为我们可以不用绑定到target而直接把
data更新到buffer中，所以只需要一个glBindBufferBase()就足够了。并且，如果我们是显式的指定UBO和SSBO在GLSL中的binding point，
每个shader中都保持它的binding point一致，那么我们只需要在创建buffer时调用glBindBufferBase()，即可一劳永逸，后面只用DSA更新
数据即可，再也不需要去管bind，所以UBO和SSBO的类里面，根本就不需要Bind()以及Unbind()的方法。

说完了bind的问题，补充一下所有buffer（包括非indexed的buffer）整体上是如何处理data的。
对于每个buffer，以前的方式是，我们用glGenBuffer()这一类的方法去创建buffer object，然后马上glBindBuffer()，趁着绑定的时候
去glBufferData分配内存并初始化data，再解绑，随后每帧，都需要先重新bind起来，用glBufferSubData()更新data，再unbind。
有了DSA以后，现代的方式是，先用glCreateBuffer()这一类的方法去创建并同时初始化对象，再用glBufferData分配内存，随后同样去更新
数据，至于每帧需不需要bind，取决于是哪种buffer，怎么用。然而，需要说明一下现代API的不同。

首先，在用了DSA的情况下，我们可以扔掉所有的glBindBuffer()，用DSA的方式去替代它，只不过对于某些buffer，我们可能不了解DSA的情况
下该怎么去call。比如你会发现，我们的VBO和IBO都没有bind和unbind方法，因为VAO中使用的都是DSA方法去SetVBO和SetIBO，所以只需要
VAO有个bind unbind的方法就行了，其他一些比较少用的buffer可能要研究一下。

其次，glBufferData()和glBufferSubData()，都可以用来更新数据，一个更新全部数据，一个更新部分数据，但如果用0作为index，用整个
buffer的size作为size，glBufferSubData()是可以完全替代前者的。需要注意，它们两个有个重要区别，就是glBufferData()不仅更新
数据，它还可能会分配内存，比如我们刚创建对象时，第一次调用的glBufferData()就会在GPU上分配内存空间，而以后每帧更新时，
glBufferSubData()只能在已经分配好的空间上修改data，相比之下，glBufferData()则没有这个限制，它每次都会invalidate之前分配的内存，
重新分配，所以我们可以传入更大的数据量。glBufferData can be used to update the data in a buffer object. However,
this also reallocates the buffer object's storage. This function is therefore not appropriate for merely
updating the contents of the allocated memory (and for immutable storage buffers, it is not possible).

除了glBufferData()和glBufferSubData()以外，还有个更新data的方式，叫做mapping，想要使用mapping，那么在glBufferStorage()
的时候，首先我们必须要传入开启mapping的bit，包括GL_MAP_READ_BIT GL_MAP_WRITE_BIT GL_MAP_PERSISTENT_BIT 和
GL_MAP_COHERENT_BIT。简单来说就是，通过glMapBuffer()把buffer的地址map到C++ memory space，让我们得到一个GLubyte*的指针，
于是在C++端，我们就可以随意的读取和修改数据（通常是用memcpy上传），改完用完了以后再glUnMapBuffer()。注意Unmap是必须的，因为在
buffer被map的期间，它是处于一个被lock锁住的状态的，GPU的rendering command将无法使用它（除非使用GL_MAP_PERSISTENT_BIT bit）
glMapBuffer()的好处是，我们可以更灵活的处理data，而不需要事先准备好一个const void* data的数组参数，而且它还提供了好多flag用于
指定修改的方式，比如GL_MAP_READ_BIT，GL_MAP_COHERENT_BIT什么的，glMapBuffer()可以干所有glBufferSubData()能干的事儿，
但它还能干一些别的事儿，比如invalidate一部分data什么的，功能更多。可以看到，glBufferSubData()相当于是自动模式，而
glMapBuffer()是纯手动模式，控制权更大但也麻烦，glMapBuffer()的坏处十分明显，就是比glBufferSubData()操作起来代码更复杂，且过
程非常容易出错，要分清楚每个flag的含义及data类型，并要确保map的期间buffer不会被其他线程的rendering command使用，容易导致许多
bug。从性能的角度来讲，glBufferSubData()和glMapBuffer()并不会有明显的区别，除非对性能要求非常高再去做profiling，两者的差别
比较subtle，涉及到synchro同步问题，涉及到内存是在C++端分配还是在GPU上直接分配，这些太高级了我不懂，总之简单来说就是，取决于你的
应用是CPU bound的还是GPU bound的，对于我们这种普通的demo渲染器，不需要关心这么复杂，永远就只用glBufferSubData()就足够了。

   （除非我们要用triple buffering，Persistent Mapped Buffers这种高级功能）

如果需要大量的streaming data，才可能要用到Persistent mapping + triple buffering，但其实性能差别也并不大，可以参考
<https://www.cppstories.com/2015/01/persistent-mapped-buffers-benchmark/>

另外，有了DSA，现代的OpenGL要尽可能的使用immutable data store来替代传统的data store，这样GPU端可以自动做很多优化来加快
速度。immutable data store就是你和GPU约定好了，我这个buffer分配了这么大的内存空间，用了这种数据format等等，这些都是固定
的属性保证不会变，我之后只会更新data的值，绝不会扩展空间或改变格式什么的。为此，我们要尽可能的避免使用glBufferData()分配空间，
而是用glBufferStorage()来替代它。注意，immutable data store对于textures而言十分重要，因为textures很大，性能提升会很大，
我们一定要用glTexStorage()来替代glTexImage()。

buffer的Invalidate方法，即glInvalidateBufferSubData()和destructor是不同的，unlike destruction, invalidate
tells the GPU to release the memory space allocated for the buffer so that it can be reused, but the object
handle (id) is kept for later use.

buffer的Clear方法，glClearNamedBufferSubData()，我们用GL_R8UI 作为internal format，GL_RED作为format,
GL_UNSIGNED_BYTE作为type，并且设置data参数为NULL，这样可以通用的fill every byte with 8 bits of zeros，这样可以保证
for both two's complement and IEEE-754 floating point, cleared values will always be 0。注意size参数is measured
in number of bytes，这样方便我们使用sizeof operator来计算size。

SSBO::Flush()，glFlushMappedNamedBufferRange()只需要在多线程的情况下，且使用了手动的persistent mapping的时候使用，
哪个线程update了buffer data，就在哪个线程call。如果指定了GL_MAP_COHERENT_BIT，我们是不需要自己flush的。

除了正常的texture以外，还有一种叫做buffer texture的东西，它不同于texture而是一个buffer，但是又不属于VBO,IBO,UBO,ATC
这种传统的buffer objects。它的target是 GL_TEXTURE_BUFFER，简单来说，texture buffers are only 1-dimensional, cannot
do any filtering and have to be accessed by accessing explicit texels (by index), instead of normalized [0,1]
floating point texture coordinates. buffer texture的data必须来源于其他buffer objects，比如我们可以把VBO的数据attach
到一个buffer texture上面，然后在shader里用texelFetch()去访问这些值。They are used as large 1D array data to be accessed in GLSL.
简而言之就一句话，buffer texture是废物，没有一点用，如今我们有了SSBO和ILS，永远都不需要用到它。它只是老版本的过时产物。

从OpenGL3开始，我们可以用Transform Feedback机制，将vertex shader或geometry shader的output写入到TFB buffer中，这样就
可以在下一帧重复利用上一帧的vertex数据，一个典型的应用场景就是particle systems。不过现代OpenGL，我们有了更强大的工具，SSBO
以及ILS，基本上不太需要用TFB，而且TFB在C++端的setup代码比较繁琐，更重要的是，我们可以把原本很多vertex shader以及fragment
shader的活分离出来，放到compute shader里去做，这样速度快很多。现代化的bloom以及particle systems，都是用compute shader
配合SSBO/ILS来实现的。

}

void PBR光学知识() {
    /* some (hopefully correct) notes for BSDF material model:

- the minimum value of roughness should be clamped to a non-zero float (like 0.045) so that the
specular highlight is always visible, this clamping must take place before reparametrization.

- metalness should be a binary value, either 0 or 1, not some floating-point number in between.
- specular reflectance (F0) is chromatic for conductors and achromatic for dielectrics.
- the Fresnel function can be seen as interpolating between F0 and F90, as HoV goes from 0 to 1
the view direction moves from grazing angle (90) to normal incidence (0), so the specular
reflectance goes from F90 to F0.

- the final appearance of a material includes 2 parts: diffuse color + specular reflectance F0
for dielectrics, diffuse color is persistent and F0 is achromatic (colorless)
for conductors, there is no diffuse color but F0 is chromatic (colored)

- the specular param controls F0, for dielectrics, it's mostly ~ 0.5, which translates to an F0
of ~ 0.04, for water, it should be 0.35, which corresponds to an F0 of 0.02, cannot be lower.
for diamonds and gems that have a high F0 of 0.10 ~ 0.16, specular can vary between 0.8 ~ 1,
for conductors, this param is not used because specular reflectance is only computed from the
chromatic F0. No real world material has an F0 < 2%, so the specular must be clamped to 0.35

- specular and IOR represent the same physical attribute, just in different ways, if one is known
the other can be computed and deduced. For metals, the specular param has no effect because
specular intensity is all about F0 (metal's albedo color). For dielectrics, it controls the
specular reflectance F0. For refractive materials, the higher the IOR, the slower light will
travel through the medium, so the light path is also bent more.

- the clear coat layer will always be isotropic and dielectric, with low roughness values.
- the clear coat layer also uses Cook-Torrance microfacet BRDF, but much simpler and cheaper.
- in this layer, the Smith-GGX visibility term is replaced by the Kelemen visibility function but
D and F stays put, and since it's dielectric only, F0 is always set to 0.04.

- ambient occlusion is for occluding ambient lights, that's why it's called "ambient", typically
it only applies to diffuse indirect lighting, such as ambient occlusion maps and dynamic SSAO,
but the specular part of shading is usually not affected (not occluded).

- to make blending easier, RGB colors should be pre-multiplied with the alpha channel.
- transmission from 0 to 1 determines how transparent a refractive object (dielectric) is, wheras
absorption from 0 to n determines the amount of light attenuation through the material, that is
how fast the object absorbs each R/G/B component of the incoming light as light penetrates and
travels through the object's interior solid volume.

- thickness represents the thickness of solid objects in the direction of normal, for plausible
results, it should be provided per fragment (as a texture) or at least on a per-vertex basis,
but for simple symmetric geometry like a sphere, we can also hack it using `NoV`.
*/

最开始学PBR这块时，看的是learnopengl的教程，它和主流的渲染引擎比起来只是一个入门教程，所以很不严谨，也不考虑能量损失什么的，不要借鉴。
learnopengl上面对于diffuse以及specular光照部分的权重区分，很简单粗暴，直接计算Fresnel项来作为specular的权重ks，然后说为了
能量守恒，diffuse的权重kd就必须是(1 - ks)，保证加起来为1，也没有考虑multi-scattering的IBL，不过在Disney最早期（2012年）
提出它的PBR模型时，这个做法确实是当时的state of the art，那个时候还没有Kulla—Conty能量守恒和Lagarde对此的进一步改进。

对于早期的PBR和现在的PBR，需要注意到一件事情。那就是，我现在的PBR的IBL部分，是参考Filament的文档的，考虑了multi-scattering和
能量守恒，考虑了布料材质，更加的科学正确，对于diffuse以及specular部分的权重，是用`E = mix(dfg.xxx, dfg.yyy, f0)`来计算的，
diffuse部分的系数则是1-E。一个最重要的区别就是，我现在的IBL计算，是不会用到specular D/F/G当中的任何一个公式的，当然Fresnel函数
也不会用到，所有的IBL部分的贡献，全部来自于预计算好的irradiance map，prefiltered environment map以及BRDF LUT。在learnopengl
的IBL里面，包括最早期的Disney提出的模型中的IBL也是，他们都是用计算出来的Fresnel项作为ks系数的，Burley在这个过程中还发现，由于我们
认为F90永远等于1，所以当我们从grazing angle去看一个哪怕相对比较rough的表面的时候（比如地板），依然会很清楚的看到skybox的反射的倒影，
也就是IBL的specular的部分，但这显得很难看很不真实，于是Burley提出了在Fresnel函数上面动手脚，在函数中考虑roughness，把本来为1的
F90 clamp到(1 - roughness)也就是smoothness，这样对于比较粗糙的表面就不会有明显的IBL倒影了。（btw，如果不是IBL而是直接光照部分，
粗糙的物体在grazing angle明显显示出specular部分是合理的，并不会造成视觉上不真实）。那么现在呢，对于我的IBL，我根本就不用Fresnel
函数，也就不可能去做这个事情了，但是我们却会在计算LD项的时候去考虑roughness。LD是怎么从prefilter_map中取的？根据roughness来取。
如果roughness为0，我们取base level，随着roughness逐渐增加，我们开始取下面的mipmap层，直到roughness为1取到最高层的mipmap为止，
也就是skybox最模糊的样子。所以说，这就是从roughness到LOD的一个映射，roughness从0到1，而LOD从0到最高层的mipmap。大多数人做这个
映射，是直接用线性映射的，即用roughness乘以最大的mipmap level，得到应该取哪个level。而我现在想在IBL中考虑roughness，就可以用
一个非线性的映射，用easing function来做，比如如果ease in很厉害的话，roughness的大部分值域都会对应到LOD的base level，那么即使
比较rough的表面也能明显看到IBL的反射，反过来如果ease out的厉害的话，roughness刚从0增加一点点，LOD的level就会急剧上升，于是大部分
roughness都会对应到比较高的mipmap，IBL就会比较模糊，只有当roughness很小时，也就是表面非常光滑的时候，才能明显看到IBL的反射。所以
说，我的IBL，需要用ease out函数去sample prefilter_map，这样就可以达到早期Burley提出的那个同样的效果。

早期那个IBL还提到一点，就是在计算Fresnel的时候，由于IBL的环境光是从四面八方来的，我们没有一个单独的L和H向量，所以要用NoV去替代
Fresnel函数的HoV参数（因为N和H通常非常接近），而现在我们根本不需要这个了。别忘了HoV == HoL，H就是L和V的半程向量。

BSDF = BRDF + BTDF
BSSRDF is way more difficult (transparency, Subsurface scattering also needs BRTF)
Microfacet Cook-Torrance BRDF没有考虑多次散射，分层材质，以及衍射
BRDF是四维的，对于一个material材质而言，roughness和F0是给定了的，BRDF只取决于入射光Li和出射光Lo，每个L都是球面二维的(phi和
theta)，所以总共是四维。算上roughness和F0的话，相当于是说，所有可能的BRDF的合集空间是六维的。BSSRDF则是更高维的，因为光入射
到一点，却会从附近的另一点remit出来，比如次表面反射，所以此时我们不再能只考虑单独的一个shading point。
关于BRDF这块，解释的最好的：<https://patapom.com/blog/BRDF/BRDF%20Definition/>

IBL: local or distant probes are used, you can't always assume entities are at world center. But, we're
focusing on distant environment probes, where the light is assumed to come from infinitely far away. For
local light probes, we need to do IBL precomputation at multiple positions and interpolate in between at runtime.

HDR env map是从HDR文件读取进来的，所以颜色值是在linear color space的，那么convolution出来的irradiance map，也是在
linear colorspace。从irradiance map中采样出来的值，和物体原本的albedo相乘即可得到diffuse IBL的部分，但是和以前一样，
还是要注意albedo必须做过sRGB到linear的转换，否则乘出来不对的。irradiance map代表的就是diffuse的值，就是一个白色物体的
diffuse color，Lambertian Diffuse Reflectance部分已经包含在里面了，所以拿到值以后，直接乘以diffuse albedo。如果你再
乘以PI分之一，等于算了两次Lambertian diffuse的成分。假如是用Spherical Harmonics，那么INV_PI需要在生成SH9系数的时候就
被包含进去，INV_PI is rolled into sh9

diffuse iraddiance map和prefiltered specular env map的异同————两者都是做convolution，做的是一个模糊操作。然而，
前者是漫反射，blur kernel的范围是整个半球，所以blur的程度要大的多，出来的图像非常的模糊，这也是为什么我们只需要较小的分辨率
的原因。后者呢，则是镜面反射，还是要保留一部分细节的，不能全糊掉，blur kernel的范围是一个较小的specular lobe所对应的立体角，
采用的是重要性采样，所以blur的程度要低很多，出来的图依然能看到一些细节，并且我们需要生成一系列mipmap来通过trilinear
filtering插值估计0-1之间的不同的specular范围，所以它的base level的分辨率不能太小。对应到数学公式上，记住前者的积分里是带
cosine项的，所以每次采样skybox的结果是要被cosine或点乘weigh一下的，后者，不带cosine项，就是对入射光Li的积分。
最后一点区别是，前者为漫反射，漫反射与观察视角也就是view vector无关，从四面八方看上去都是一个值，因此在查找texture时，是用
法线N去查找的。而镜面反射的值取决于观察角度，不同角度看结果不一样，假如L固定，那么具体眼睛看到的，是L经过N反射为R，R向量打进我们
的眼睛里的值。而由于光路可逆性，所以当观察向量V固定时，V经过N反射为R = reflect(-V, N)，相当于是本来的入射光L，这才是我们应该
用来去查找texture的向量，是用R而不是用N。不要再搞错镜面反射了，镜面反射不用N去查找，想象一下你在湖边看夜景，你看到的肯定是远处
的高楼大厦和山的倒影，而不是湖面正上方天空中的星星月亮。

在analytical light光照的部分，我们知道每个光源的方向L，也知道观察角度V，所以可以求出half向量H。在IBL光照中，光来自于四面
八方，由于没有一个具体单独的L，我们不知道L，只知道V，就无法得到H。此时，一切和H有关的角度都是用N去近似的，比如HoV换成NoV。

by convention, all vectors are pointing outwards, from the shading point (fragment) to the light source,
doing so is convenient.

环境光这块目前还是主要用IBL来做的，有的用SH来处理diffuse，但是SH是无法处理specular的，所以还是要IBL，除非整个场景只有
diffuse的物体。用了SH的话，我们就不需要irradiance map了，而是可以通过SH函数在runtime去evaluate每个shading point的
diffuse部分。SH的具体做法和代码，在OpenGL Development Cookbook 2013这本书里面有的。也可以参考Filament，在libs文件夹
里有C++代码实现。比IBL更加好的方法，是LTC shading，它是用来算面光源area light的shading的，
单位半球上对常数1积分是2pi，单位球上积分是4pi。这个就是球体的表面积公式。单位半球上对cos积分是pi。

radiance is irradiance from a specific direction (due to the per solid angle definition)
diffuse其实在物理上就是subsurface scattering(SSS)，只不过我们通常用BRDF把它简化了。真正的次表面发射是，入射光进入物体
表面上的一个点，经过物质内部原子的一系列碰撞反弹，从另一个点remit出去，这个点一般就在原来的入射点的附近，可能差几个像素，但
进出并不是同一个点。而BRDF做的简化就是，尽管入射点出射点不一样，但他们的位置很近，如果两个点在一个像素内，相当于两者的距离小
到可以忽略，那么就可以认为入射出射都在同一个点，就可以用简单的BRDF来描述，可以在同一个点locally的计算shading，跳过了SSS。
然而，如果一个pixel很小（高分辨率），且入射出射点的距离明显大于pixel的大小，就不能用BRDF的diffuse来描述了，需要用BSDF=
BRDF+BTDF来model，也就是次表面反射。而如何去model这个距离以及入射出射方向的变化，需要用到BSSRDF。

IOR是一个复数，实数部分代表了光在该均匀介质中的传播速度，虚数部分代表有多少光会被该介质吸收。IOR是用于描述任何均匀介质的。
reflect反射，refraction折射，diffraction衍射。。。。

Light is composed of electromagnetic waves. electric and magnetic always come in pairs. So the optical
properties of a substance are closely linked to its electric properties = magnetic properties.

注意reflection和refraction是互斥的，被微表面bounce off掉的光子就不可能进入物体表面，所以当有refraction的时候，它只会
从diffuse的部分中偷取一些贡献，和diffuse分担贡献，但不会影响specular部分的高光。
对于refraction，需要注意，transmission在0-1之间，代表refraction会从diffuse中偷取多大比例，这取决于物体的透明程度。
而当给定transmission了以后，具体的折射情况由剩下几个参数决定，其中thickness是volume的最深的厚度，比如球体就是直径，而
transmittance是一个linear RGB的值，代表光在介质中传播时，哪些波长的颜色wave会被吸收（剩下的继续传播），这个颜色可以和微
表面的base color即albedo相近，但也可以和albedo完全不同，它取决于具体是哪种介质，比如你给一块冰块外面涂了层番茄酱，表面的
albedo是红色，但冰块内部的transmittance仍然是白色，因为H2O会把光完全吸收。另外，要知道IOR和物体的密度有关，密度越小IOR
越接近1（如真空和空气，以及各种其他气体），光被折射的比较小，密度越大IOR也越大（比如水银，汞温度计），光被bent弯曲的非常厉害。
需要特别注意一下tr_distance这个参数，即transmission distance，它代表的是光在该种介质中可以传播的距离，这个距离和volume
的thickness是无关的，而且通常要大的多，对于越是密度大dense的介质（高IOR），光受到的阻力越大，被bent弯曲的越厉害，能量和颜色
attenuate衰减的也越快，所以tr_distance会比较小，反过来，对于密度小sparse的介质（低IOR），光受到的阻力很小，几乎不怎么被弯
曲，能量和颜色的衰减也越慢，所以tr_distance非常大，在真空中是无穷大，即光在宇宙中可以无限传播，在空气里也很大，但会被空气中的
杂质慢慢稀释，在水里则相对小一些，所以再清澈的海域，阳光也传不到海底，水下20米左右的地方就变得很暗了。

DFG or DFV的本质，其实就是Fresnel effect，就是specular reflectance，重点在于Fresnel项的值。而N项和G/V项的作用只是用
于决定Fresnel effect在什么地方出现，会不会被遮挡，可见度如何。记住DFG代表的就是specular。

在IBL中，split-sum所估计的渲染方程，通常写成（参考 GAMES202_Lecture_05.pdf）
Lo = diffuse                 + specular
   = irradiance_map (or SH9) + prefiltered_map * BRDF_LUT;
   = irradiance_map (or SH9) + LD * DFG;
其中，irradiance_map是带cosine项的，积分和常数diffuse乘积，或者用SH9实时估计（SH9系数在C++端预计算后作为uniform array传给GLSL）
prefiltered environment map通常被叫做 LD 项，因为它不含cosine，就只是分子对 L 积分，再除以分母对 D 空积分
BRDF LUT通常被叫做 DFG 项，因为它就是对BRDF乘以cosine积分，而BRDF就是D*F*G.
split-sum的核心思想，就是把Fresnel提到前面去，让DFG再拆成两项的和，去打表，如果是布料的话，再多加上一项。
重点的是DFG的前两项怎么分，GAMES 202已经讲过了，但分法不是唯一的，Filament为了考虑能量守恒，换了一种分法，使得可以直接用
DFG.xxx和DFG.yyy计算出能量补偿的系数。最终的完整形式是
Lo = SH9 + LD * (DFG.xxx * (1 - F0), DFG.yyy * F0) * energyCompensation
   = SH9 + LD * mix(DFG.xxx, DFG.yyy, F0) * energyCompensation;
最后注意，这里的mix(DFG.xxx, DFG.yyy, F0)，也就是DFG的具体值，如上所述，就是对BRDF乘以cosine积分，它所代表的含义是，
当Li=1，也就是四面八方过来的都是full white的光时，当前shading point根据BRDF积分出来是多少，换句话说，它代表了specular部分
的总能量 E，如果 E < 1，就说明有能量损失（因为Smith G项只考虑了single bounce），而损失的能量是(1 - E)，我们会通过
energyCompensation把它补回来。另外，这也代表了，specular部分的系数永远是 E，剩下的系数(1 - E)，是分给diffuse的，这样做才
科学，而不是像learnopengl那样naive的把Fresnel F项当成是ks，把（1 - F）当成kd。假如有refraction的话，specular并不会受影
响，该有Fresnel高光的地方还是有，因此refraction需要从diffuse中去偷来一些contribution，也就是说，此时specular的系数还是 E，
而diffuse和refraction合起来的系数是（1 - E），具体的话，refraction的系数是（1 - E）* transmission，而diffuse的系数是
（1 - E）* (1 - transmission). 这次IBL应该彻底懂了，理解透彻了。

specular部分，无论是IBL还是直接的analytical光源贡献，都是用Cook-Torrance BRDF计算的（IBL的话是在prefiltered envmap
中利用了Cook-Torrance），而Cook-Torrance并不能考虑multiscattering的情况，因此会有能量损失，当物体越是diffuse或越rough，
multiscattering出现的频率越大，损失的能量也越多。Filament的解决方案是用Kulla-Conty17+Largarde18的paper提到的办法，他们
发现能量补偿的计算正好可以和IBL共享，所以在做IBL预计算的时候，用了我目前做的这种方式去拆分split-sum（这和GAMES 202以及
Unreal提出的原版split-sum公式不同，但验算后是等价的），从而可以通过IBL的BRDF LUT顺带计算出energy compensation项的系数Ec，
保存在pixel.Ec中。之后，为了补偿能量，我们只需要在Fr上面乘以Ec即可，注意只在Fr上面乘，因为损失的能量来源于specular部分。另外
注意，虽然Ec是从IBL中得来的，但它只是利用了IBL的计算过程搭了个便车，使得可以从BRDF LUT中得到，所以实际上只和材质本身的BRDF有
关，和IBL无关，因此，Fr*Ec不是只在Evaluate IBL的时候应用，在算点光源这些analytical光源的时候也要应用，都是要乘以Ec的。

Diffuse部分，我们通常直接用Lambertian或者Burley计算Fd，不用套用Cook-Torrance BRDF，比较简单。对于Fd，也不用考虑什么能量
损失。然而实际上要知道一下，其实漫反射是有一小部分是被reflect掉的，而Lambertian这种并不会考虑，所以其实Fd是有能量过剩的，即
energy gain，正确的做法应该去减掉（attenuate）一部分的diffuse，也就是在Fd上面乘以另一个Ea系数。只不过，这部分比较微小，也
没人提到，通常直接忽略即可。

关于Ambient Occlusion，简称AO，要明确一下。它代表的是环境光遮蔽，0的话说明IBL对本材质的贡献为0，本材质不受IBL影响，1的话
说明完全吸收IBL的贡献。那么什么才是IBL的贡献呢？越是光滑的物体，等于说越是specular，那么越是会大量反射IBL的环境光，受IBL影响
越大。反过来越是diffuse的物体，越粗糙，环境光大部分都被材质吸收掉了或者在multiscattering中被遮挡掉了，因此受IBL影响越小。
所以要理解，所谓的AO，实际上是diffuse AO，即AO是只针对diffuse的部分应用的，所以是乘在Fd上，和Fr无关。环境光遮蔽，我们不会去
遮蔽specular的部分，specular有的只是物体本身几何遮挡的一些阴影，那是shadow而不是AO。由于AO是只针对微表面模型的，无法考虑宏观
上物体的几何遮挡关系，因此大的遮挡我们用shadow做，很多小的呢，就用SSAO和GTAO这种去解决，但这些都只是hack，物理上正确的做法在
学习光追的时候就知道了。也有人提到过specular AO的概念，不过这部分的资料很少，目前还不太理解，一般都不会考虑。

}

void CRTMemoryLeakCheck() {
    为了检测内存泄漏并能让报告显示泄露的具体脚本和行数，按照CRT的文档，需要加上以下代码
    #ifdef _DEBUG
        #define new new ( _NORMAL_BLOCK , FILE , LINE )
    #else
        #define new new
    #endif
    需要注意的是，在定义了_CRTDBG_MAP_ALLOC宏之后，以上的这段代码，并不是放在main里面就可以了。每一个你想要报告显示行数的脚本里，
    都要在开头加上这段代码，否则不会显示行数，只会显示一个<normal block>。我们可以在每个脚本里都加上这段代码，也可以加在pch.h里。
    值得注意的是，只有当我们知道存在内存泄露的时候，再去用这段代码debug定位泄露的位置，只加在可疑的脚本里，解决了问题之后就删除。
    release build的时候，不要开启CRT报告，但这不是重点。重点是，通过定义宏的方式去覆盖new操作符，是一个非常危险和ugly的做法，要
    极力避免，不让它出现在我们的代码里，除非是具体debug内存泄露的时候再用。

static变量在C++中，是由C++ runtime来管理的，它在进入main之前被construct，在main返回也就是程序结束之后被destruct，我们
代码无法控制，所以很危险。尽量避免使用static变量，尤其是全局的，以及会分配内存和依赖于其他组件的变量，否则等到它被销毁的时候，
都已经是程序结束的时候了，许多上下文都没有了。如果你启用了CRT的memory leak检测的话，memory leak报告是在程序结束前的最后被调用的。

}

void WhyNotDeferredShading() {
    deferred shading做不了什么？——MSAA和其他抗锯齿，而且有两个严重的问题。一个是如果scene中的每个物体用的是不同的lighting
    shader，你在最后的lighting pass就必须要对物体分类计算光照，因为一个quad只能套用一个shader，所以这个shader中就要处理所有
    不同的lighting model，这就要求你在G-buffer的时候，必须还要记录一下每个fragment对应的是那个物体，非常麻烦。还有一个最严重
    的问题是，我们只有screen space的信息，根本没有办法计算透明物体的光照
}

void GLSL() {
    GLSL中有一堆关于shadow的sampler类型，比如sampler2DShadow，samplerCubeShadow，这些是专门用来做shadow mapping的，和
    一般的sampler不一样，当访问这类sampler时，用的查询向量是不同的，同时它们还多接收一个参数，用于和texture当中的深度值做比较，
    并且返回的结果并不是texel的值，而是0或1，代表是否被遮挡，使用这类sampler时还需要先激活texture comparison mode，否则的话
    没用。听上去挺复杂的，其实这些特殊类型是用于做hardware自带的shadow mapping的，等于说是调用了硬件内部自带的shadow mapping
    算法的实现，可能会稍微快一点，但我们没必要去了解，我们只需要普通的sampler2D和samplerCube，自己做shadow mapping就好了。
    需要的话参考https://github.com/PacktPublishing/OpenGL-4-Shading-Language-Cookbook-Third-Edition/blob/master/
    chapter08/sceneshadowmap.cpp中的代码，以及shader中的textureProj的用法。

注意，image load store只适用于color image format，比如一般的texture和framebuffer的color attachments，但是ILS无法
适用于depth或者stencil texture，也就是说，不可以把一个FBO的depth buffer绑定到ILS上，因为ILS没有与GL_DEPTH_COMPONENT24
等格式对应的image format。

重新好好理解一下矩阵的transform转换！！！比如说，假如我们有一个新建的sphere entity，它有一个Transform component，表示为T。
那么T是干嘛的？是用来移动这个球的。原来球在世界原点，也就是在自己的local model space，现在我们把球的每个vertex左乘上T的矩阵，
就得到了球移动后的新的世界坐标。换句话说，这不就是model matrix嘛，没错。可以想一下，如果T只是向x轴移动+5，T矩阵的最后一列就是
[5, 0, 0, 1]，于是左乘T会使每个vertex都向x轴移动+5，没问题，反过来，可以用网上计算器试验一下，T的逆矩阵的最后一列，就是
[-5, 0, 0, 1]，于是左乘inverse T会使每个vertex都向x轴移动-5，又回到了原点。换句话说，model matrix的逆矩阵，是把一个world
space的物体转换回其model space（即以原点为中心）的。如果是其他物体的model matrix的逆矩阵，那么就是从world space转换到那个
物体所在的local model space。
通常，在描述中，T的矩阵被称为是一个物体的world transform，因为它直接表示了物体在world space的世界坐标。对于rotation，
scaling等等，都是这样。在公式计算中，我们称之为model matrix。这两个概念是一回事。

以上的分析同样适用于其他的entity，如果我们把sphere球换成camera相机，此时T代表的是相机的world transform。
按照前面的逻辑类比，相机的每个local vertex左乘T的矩阵以后，就得到了相机该vertex的世界坐标，没错，相机也只是一个普通的entity
物体而已。反过来呢，世界坐标中任何一个vertex左乘T的逆矩阵以后，也就是相机的model matrix的inverse矩阵，相当于是把该world
space的物体转换回到了相机的model space里，而相机的model space就是view space，换句话说，相机的model matrix的逆矩阵，就是
我们常说的view matrix，也就是我们通常所理解的从world space转换成camera space。总之记住，一个物体A的model matrix的逆矩阵，
就是用来把其他的世界坐标转换到A自己的local space的。

不仅相机如此，对于骨骼动画也是如此。在一个humanoid的模型中，有一个hierarchy的node graph，每个node有一个local的
transform矩阵，它是相对于自己的parent node的（root的该矩阵就是identity）。单独只考虑一对node，parent是p，child是c，此时
相当于是，把c看成一个物体，把p看成是world世界，而c的local矩阵就是c中的vertex相对于世界p的transform，是c这个物体的
"world transform"，所以c的这个local矩阵，是把c所在的local space中的任何一个vertex，从space c转换到它的parent p的
space里面去的。对于一个node c，只要我们沿着parent一路往上搜，一路左乘每个parent的transform矩阵，一直到root，最终就会把
一个vertex从space c转换到该humanoid模型的model space（也就是bind pose，或叫做T pose）里去。
而我们又知道，load模型的时候，所有的vertices都是定义在bind pose的，在model space里，那么对于一个node c来说，假如它的
parent分别是b，a以及root，对于任意一个模型中的vertex（此时它定义在bind pose），然后左乘root的transform矩阵转换到root
所在的local space（等同于model space，因为root的该矩阵为单位阵所以乘完还是在bind pose），然后左乘a的transform矩阵转换
到a所在的local space，然后左乘b的transform矩阵转换到b的space，最后再左乘c的transform矩阵，于是就转换到了c这个node的
local space了，假如c是animation中所包含的一个骨骼，那么我们就把原来bind pose的一个vertex转换到了骨骼c的bone space了，
接下来就可以做keyframe的interpolation。

stencil buffer主要是用来画物体的边界的，比如选中物体。还可以用来制作场景过渡效果，比如fading，圆圈式缩放，不过主要还是用
来画边界，还有一个是画shadow。更有用的是，stencil test可以很容易的判断任何形状的物体的边界，比如，drawing textures
inside a rear-view mirror so it neatly fits into the mirror shape。stencil testing通常是配合多个pass和多个
framebuffer一起使用。
一个动态的魔法传送门，门的内部可以用stencil test去贴图

GLSL的uniform，可以在声明的时候同时给个默认值，作为初始化的值，直到C++端通过SetUniform修改为止，该值都不会变。
这是OpenGL文档里有明确写的，然而现实是，很多驱动并没有做这个功能，我的显卡上，只有compute shader的uniform可以有默认值，
其他的shader无论是否设置了初始值，实际上存储的值全部是0.0，所以要特别注意，保险起见每个uniform都至少设一次值，不要依赖于驱动的初始值。

compute shader如何分配资源？在一个work group中，总共有local_size_x * local_size_y * local_size_z次shader
invocations，这是单独一个work group的工作量，而这些invocations一定是run in parallel的，只不过local_size有一个上限，
比如当local_size_x = 40时，我的AMD显卡就会报错out of limit，好点的显卡可能会高一些。同一个work group中的invocations
相当于时threads，每个invocation对应一根线程，他们可以共同读写一块shared内存区域。
当我们dispatch的时候，Dispatch函数的参数是work group count，也就是我们的总计算量去除以一个work group的local size来得
到的。假如只考虑某一维度，该维度上有5000个数需要计算，而一个work group在该维度上的local size是100，那么我们就需要dispatch
50个work groups。Work groups之间的运行顺序也是随机的，只不过他们不一定是并行跑的，只能说driver会尽量让他们并行，但不保证。
于是问题来了，怎么分配计算量，才能得到最高的效率呢？如何设置最优的work group的local size？这个问题的答案比较复杂，一般只能试了
才知道，但有几个原则可以借鉴。

1. 如果把local size设置成1，layout(local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
也就是说，每个work group只有一次invocation，一根线程，那么我们需要很多很多的work groups，得到的速度一定是最慢的。compute
shader的性能提升来源于并行的power，是做batch update，但上述这种情况，每个work group是一个batch，但每个batch只有一次计算，
等于是没有做batch，自然最慢。不仅如此，驱动程序中dispatch每一个work group是需要一定的overhead和开销的，如此一来我们最大化了
开销，那么当然是最慢的。

2. 于是，stackoverflow上有人说，最优的分配方案，是最大化每个work group的local size，最大化并行，减少dispatch work
group的overhead和开销。理论上，这样理解应该是对的，起码不会比最优慢很多。我实际试了一下，假如硬件对于local size的limit是32，
那么设成32确实很快，但设成10也并没有慢多少，速度几乎是一样的，这里的原因就比较复杂了，有比如driver的优化，GPU的具体运作方式等等。
我觉得，只要local size设置的偏大，比较靠近limit，就可以了。

3. 按照CS的以往惯例，当参数是2的指数倍的时候，通常是最快的。所以local size尽量设置成2的倍数，比如16，32，64这种，而不是10，20。
另外一个方面是，整数肯定是比浮点数要快的，所以分配任务时尽量要凑整，保证每个work group的规模完全一致。比如我们总共有1000个计算
量，是固定死的，那么假如local size设置成32，1000除以32等于31.25是除不尽的，会余下8，此时我们需要32个work group，前31个
group都分别有32个计算量，而最后一个group只有8个计算量，导致work group之间不是完全均匀的，这种情况往往会慢一些，最主要的是，
它会引入一个corner case，使得我们的程序代码更容易出错，要尽可能避免。假如1000个计算量是给定的，那这时我们宁可把local size
设置成10，以保证correctness，如果可以的话，应该把总计算量也改为2的倍数，比如1024，2048，而不是1000。

LOD代表的是Level of Detail的意思，也就是说，LOD越大，details越多，通常表示物体离相机越近，反之，LOD越小，细节越少，
通常表示物体离viewer越远。从近到远，level of details是在逐渐下降的，越远的物体越模糊，越缺少细节。
通常当我们提到LOD时，我们说的是gemometry mesh的细节或者是texture的细节。
注意，不要把LOD的概念和GLSL中的lod参数给混淆了，在GLSL中，比如textureLOD()的lod参数这种，实际上代表的是mipmap level，
因为OpenGL(Vulkan也是如此吗？)对lod的定义指的就是mipmap level，lod=0代表的是texture的base level，细节最多，而lod=1,2,3...
并不是说level of details在增加，而是指用更高level的mipmap，所以对应的level of details是变得越来越小的。
如果只是提到图形学意义上的lod的概念，如果用lod=0代表最高的level of details，那么其余的lod应该是-1,-2,-3,...,-1000这种负的。

在C和C++中，浮点数的默认类型是double，所以3.14159是double，除非显式的加上f，变成3.14159f，这时编译器才认为它是float。
同样的，整数的默认类型是signed int，当我们写3的时候就是int的3，而3U才是unsigned int的3，3L是long，等等。
在GLSL中，整数我们不需要去关心后缀，而对于浮点数，GLSL的默认类型就是float，所以写浮点数不要在加上f的后缀，3.14直接就是float。
假如我们在GLSL中要用double，那么此时就必须要显式的加上lf的后缀，代表long float即double，所以3.14lf才是double。
在C++中，3f这种写法是合法的，编译器会帮你补全为3.0f，是个浮点数，在GLSL中，编译器不会帮你，3f是整数加f后缀，是非法的，直接编译错误。

在写GLSL shader代码的时候，尤其是fragment shader的时候，我们要特别注意控制代码的分支判断，减少if-else branching。
对于vertex shader来说，每个vertex被invoke一次，如果vertices比较少，那么其实无所谓，对于fragment shader，它的invocations的
数量通常是vertex shader的几千几万倍，所以尽可能避免任何的if-else。
有两种办法，第一个，当不同的fragment可能要调用不同的函数时，可以考虑用subroutine uniform来替代。
第二个，有些简单的比大小的判断，或是在不在某区间内的判断，可以用step()函数来替代。
现代的GPU对于分支的优化比较好，所以差别其实不会太大，但还是要养成好习惯，多用step()函数。

由于我们用了自己的material系统，material会自动解析shader中的uniform并创建每个location的uniform对象。在创建时，每个uniform
的初始值都会被设置为0（value(0)）或用0来构建glm的数据类型，所以要记住，我们是无法依赖于GLSL中的uniform的默认值的，这个默认值也
无法被query到。对于每个uniform，我们都要确定自己手工的有去设置uniform的值。

struct self_t {
    mat4 transform;      // 1000, model matrix of the current entity
    uint material_id;    // 1001, current mesh's material id
    uint ext_1002;       // for future extension
    uint ext_1003;       // for future extension
    uint ext_1004;       // for future extension
};

layout(location = 1000) uniform self_t self;
这里我们定义了一个struct，并声明了一个该struct类型的uniform，由于它是complex type，所以会占据多个uniform的location。
我们指定了location=1000，所以transform对应的是1000的位置，接下来每个struct member依次取下一个位置，也就是，material_id
对应1001，等等。注意，尽管我们定义了一个struct，它并不是一个block，和uniform block完全不是一个概念。而且，在shader去parse
active uniforms的时候，它会把struct看作是分开的一堆uniform。比如我们使用了self.transform，那么shader会认为location=1000
是一个active的uniform，但它并不会认为整个self_t的struct都是active的！假如你没有用ext_1002，那么location=1002就不是active的，
会被GLSL编译器optimize out！
说到底，在GLSL中定义struct，只是为了方便我们人去看，把变量做归类，但在GLSL编译器的眼里，每个成员就和单独的uniform没有区别。

shader.SetVec3("Material.diffuse", world::unit);  // set a member of the struct in GLSL
shader.SetMat4("MyArray[1]", world::eye);  // set a member in the array in GLSL (MyArray is an array of mat4)

对于GLSL shader，const变量是不会被不同的shader stages之间shared的，也就是说，你在vertex shader里定义一个const变量，不会
被fragment shader看到，哪怕你在fragment shader定义了一个一模一样的同名变量，那也是另一个变量。

当你的程序里有多个不同的shader program，这些program之间是完全独立的，他们里面的任何同名变量都不会被share，包括uniform，
所以你在query location和赋值的时候，要对每个PO都分别操作一次，除非使用uniform buffer object。

假如你定义了一个没有被shader程序用到的变量，那么GLSL编译器会自动remove这个变量，于是你用glGetUniformLocation去query它的
时候，结果会返回-1（但并不是报错），然后程序正常运行却可能会显示黑屏。

transform矩阵通常是用GLM在C++代码中算好, send it to GLSL, 在GLSL里只做multiplication乘法。
GPU对矩阵乘法是优化过的，矩阵乘法都要放在shader里（主要是vertex shader，对每个vertex apply）。
经过shader后，GPU硬件中的厂商的OpenGL代码会自动计算"divide by W"的步骤

Try to not overburden the fragment processors of your GPU.
it is recommended to do computations in the vertex shader rather than in the fragment shader, because for
every vertex shader invocation, the fragment shader could be invoked hundreds or thousands of times more.
(this is because the number of fragments is far more >> than the number of vertices, think of fragments as pixels)

尽可能的多使用Swizzle操作，Swizzle masks are essentially free in hardware
Swizzle有三种表示方式，随意使用，xyzw, rgba, stpq

除法是比较昂贵的，通常需要cost额外的计算cycle，可能的情况下，尽量改成做乘法
vec4 x = (value / 2.0f);
vec4 x = (value * 0.5f);  // much faster

同样的操作，尽可能使用built-in的函数，不要自己计算，built-in的函数是优化过的，要快很多
mix和smoothstep都是在两个数之间插值interpolate，但是mix是线性插值，而smoothstep用的是更加平滑的Hermite插值算法，插值曲线
类似于sigmoid函数的形状。
x = a * t + b * (1 - t);  // slow
x = mix(a, b, t);         // fast
x = smoothstep(a, b, t);  // fast

vec3 a;
value = a.x + a.y + a.z;        // slow
value = dot(a, vec4(1.0).xyz);  // fast

}


























































































