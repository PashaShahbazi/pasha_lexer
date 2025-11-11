
# Lexical Analyzer (Lexer) — Compiler Design Project

This project implements the **Lexical Analysis** phase of a compiler for a custom-designed educational programming language.  
It was developed as part of the *Compiler Design* course project.

> Note: This project was recently uploaded but was originally developed during my studies.

---

## 📖 Overview

The **Lexical Analyzer (Lexer)** is the first step of a compiler.  
It reads the source code and converts it into a sequence of **tokens** — meaningful units such as keywords, identifiers, numbers, strings, and symbols.

In this project, each token type is recognized using **Deterministic Finite Automata (DFA)** manually designed for every keyword and lexical rule.

The implementation is written in **Python 3**, and outputs three text files containing the extracted tokens and identifiers.

---

## ⚙️ Language Specification

The custom language designed for this project follows these rules:

### 🔹 Identifiers
- Must start and end with `&`
- Can contain letters, digits, `_`, `@`, or `#`
- Examples:
  &x&  
  &name123&  
  &value_1&

### 🔹 Numbers
- Integers or fractional numbers separated by `/`
```text
12
3/5
231/41221

```  
### 🔹 Strings
- Enclosed in double quotes: 
```text
"Hello World"
```

### 🔹 Keywords
| Keyword | Meaning |
|----------|----------|
| `repeat` | Loop structure (`while` / `for`) |
| `func` | Function definition |
| `ritorno` | Return statement |
| `verd` | Boolean declaration |
| `se` | If statement |
| `alse` | Else-if |
| `al` | Else |
| `en` | In / Range loop |
| `bro` | Function call |
| `ilg` | Numeric variable declaration |
| `rango` | Range definition |
| `caden` | String variable declaration |

### 🔹 Operators and Symbols
`+`, `-`, `|`, `^`, `<-`, `=` , `>`, `<`, `:`, `[`, `]`

---

## 🧠 Implementation Details

- **Language:** Python 3  
- **Approach:** DFA (Deterministic Finite Automata) implemented via `match-case`  
- **Dependencies:** `pandas`, `re`, `copy`

### 🔸 Main Functions
| Function | Purpose |
|-----------|----------|
| `is_symbol()` | Detects symbols and operators |
| `is_string()` | Detects string literals |
| `is_number()` | Detects integer and fractional numbers |
| `is_Id()` | Detects valid identifiers enclosed by `&` |
| `repeat()`, `func()`, `verd()`, ... | Individual DFA implementations for each keyword |

### 🔸 Output Files
| File | Description |
|-------|-------------|
| `Tokens.txt` | Raw token stream |
| `Tokens_table.txt` | Table of all recognized tokens |
| `id_table.txt` | Table of unique identifiers |

---
## 🧩 Example Files
### ✅ **Valid example:** 
`example.txt`
```text
ilg &number1& <- 8/2
caden &greeting& <- "Hello"

func &add_numbers& < > :
[
  ilg &a& <- 5
  ilg &b& <- 3/2
  ritorno &a&
]

repeat
  bro &add_numbers&
en

verd &flag& <- 
```
Running the lexer on this file produces all token files successfully, with the message:
```bash
✅ Lexical analysis completed successfully!
Generated files:
 - Tokens.txt
 - Tokens_table.txt
 - id_table.txt
```

---

### ❌ **Error example:** 
`examples/example_error.txt`
This file intentionally contains lexical errors to test the analyzer’s error handling:
```text
ilg &num <- 8/2
&name& @@ 9
funcc &x& <- 2
caden &msg& <- "Unfinished string
&partname
```
Expected behavior:
The lexer will prompt for correction or stop with an error message such as:
```bash
error in line 1 and lexim &num your variable is not complete
do you want me to complete it for you :) y/n
```

---

🧪 How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run the analyzer:
```bash
python3 pasha_lexer.py
```
3. Enter the input file when prompted:
```bash
Enter the file name.txt-> example.txt
```
4. Output files will be generated automatically in the project directory.
---
## 🔄 Keyword Generator Project

The keyword functions used in this lexer (like `repeat()`, `func()`, `verd()`, etc.)  
were **automatically generated** using a separate project that converts **regular expressions** into **Deterministic Finite Automata (DFA)** and then creates corresponding **Python functions**.

That project was built to automate the repetitive task of manually coding each DFA in the compiler design process.

👉 Related project: [**DFA2Code**](https://github.com/PashaShahbazi/DFA2Code)
