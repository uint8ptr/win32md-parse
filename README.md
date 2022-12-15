# WinAPI parser

WinAPI definitions in a easily readable format, with a python parsing library included.

The function and type were definitions exported from [Win32Metadata](https://github.com/microsoft/win32metadata) (the version present in the repo is 38.0.19-preview).

## Installation

The parser uses the [Lark](https://lark-parser.readthedocs.io/en/latest) library, so you need to install first:

```
pip install lark
```

## Usage

The parsing library is contained in the file `parser.py`, and provides the functions `parse_function`, and `parse_type`, which return a dictionary with the parsed data:

```python
In [1]: import parser

In [2]: parser.parse_function('BOOL VirtualFree([In] [Out] void* lpAddress, [In] nuint dwSize, [In] VIRTUAL_FREE_TYPE dwFreeType);')
Out[2]: 
{'args': [{'attrs': [{'name': 'In', 'params': []},
    {'name': 'Out', 'params': []}],
   'type': 'void*',
   'name': 'lpAddress'},
  {'attrs': [{'name': 'In', 'params': []}], 'type': 'nuint', 'name': 'dwSize'},
  {'attrs': [{'name': 'In', 'params': []}],
   'type': 'VIRTUAL_FREE_TYPE',
   'name': 'dwFreeType'}],
 'varargs': False,
 'return_type': 'BOOL',
 'name': 'VirtualFree'}

In [3]: parser.parse_type('typedef byte BOOLEAN;')
Out[3]: {'name': 'BOOLEAN', 'def': 'byte'}
```

## Folder structure

- `functions/`: API definitions, grouped by DLL name
- `types/`: data types, grouped by category

## Limitations

In the current state, all type identifiers can only be composed of one word and the `[]` operator is not supported.

Examples of valid definitions:

```C#
int number
HWND hWnd
void * memory
char** argv
```

Examples of invalid definitions

```C#
unsigned long number // can't use two words for type definition
char argv[] // [] are currently not supported
```

## Function definition format

Uses a format similar to the one used in the MSDN documentation, to make it easy to write new function definitions and correct existing ones.

All function arguments support attributes (even with attribute parameters) and optionally variadic arguments, but not function attributes.

### Examples

Function with variadic arguments:

```C#
WIN32_ERROR TraceMessage([In] ulong LoggerHandle, [In] TRACE_MESSAGE_FLAGS MessageFlags, [Const] [In] Guid* MessageGuid, [In] ushort MessageNumber, ...);
```

Function using attribute `MemorySize` with parameter parameter `BytesParamIndex`:

```C#
BOOL WriteFile([In] HANDLE hFile, [Const] [MemorySize(BytesParamIndex = 2)] [In] [Optional] void* lpBuffer, [In] uint nNumberOfBytesToWrite, [Out] [Optional] uint* lpNumberOfBytesWritten, [In] [Out] [Optional] OVERLAPPED* lpOverlapped);
```

## Data type definitions

At the moment, only native type definitions (typedefs) are parsed and supported correctly.

### Native type definitions

Used to alias a data type to a native type.

All definitions use C# native types, but all instances of `char` (which in C# represents UTF-16 characters) were renamed to `wchar` for clarity and consistency.

```C#
typedef nint HANDLE;
```