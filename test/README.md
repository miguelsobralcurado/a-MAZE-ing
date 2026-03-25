*This project has been created as part of the 42 curriculum by <msobral-@student.42lisboa.com>.*
<br/><br/>
<h1 align="center">🧩 push_swap</h1>

<p align="center">
  A high-performance sorting engine using two stacks and a minimal instruction set.
</p>

<p align="center">
  <img src="https://img.shields.io/github/languages/top/miguelsobralcurado/push_swap?style=for-the-badge" />
  <img src="https://img.shields.io/github/languages/code-size/miguelsobralcurado/push_swap?style=for-the-badge" />
  <img src="https://img.shields.io/github/last-commit/miguelsobralcurado/push_swap?style=for-the-badge" />
</p>

---

## 📌 Description

**`push_swap`** is a 42 project whose objective is to sort data using a limited set of stack operations. It features a sorting algorithm that outputs an optimal sequence of instructions to sort a stack of integers using two stacks, **a** and **b**.

You start with stack **a** initialized with a random list of positive and/or negative **unique integers**, and stack **b** is initially empty.

The challenge is to sort stack **a** in **ascending order (from top to bottom)** using the **least number of operations possible** from the defined instruction set.

This project focuses on:
- Algorithmic thinking
- Complexity optimization
- Data structure manipulation
- Low-level C implementation

You must sort stack `a` in ascending order using only the following instructions:

| Instruction | Description |
|-------------|-------------|
| sa | Swap first 2 elements of `a` |
| sb | Swap first 2 elements of `b` |
| ss | sa and sb |
| pa | Push top of `b` to `a` |
| pb | Push top of `a` to `b` |
| ra | Rotate `a` up |
| rb | Rotate `b` up |
| rr | ra and rb |
| rra | Reverse rotate `a` |
| rrb | Reverse rotate `b` |
| rrr | rra and rrb |

---

## 🚀 Instructions

### 🛠️ Requirements

- A C compiler compliant with the C99 standard.
- `make` utility.

### ⚙️ Compilation

Clone the repository:
```bash
git clone https://github.com/miguelsobralcurado/push_swap.git push_swap
cd push_swap
```

For push_swap run:
```bash
make
```
This will produce the push_swap executable for the mandatory part.

For bonus checker run:
```bash
make bonus
```

To clean up object and binary files:
```bash
make clean      # Removes object files
make fclean     # Removes object files and executables
make re         # fclean then make all
make rebonus    # fclean then make bonus
```

## 🧠 Algorithm

This project uses a custom-designed sorting strategy optimized for the limitations imposed by the stack-based operations from the subject.

### Strategy Overview
Most high performing sorting algorithms can't be applied to this project because of the subject specifications.
Algorithms like the radix, quicksort or mergesort can't be used in their pure form because they either need more then 2 stacks or other special mechanisms.
Because of that my algorithm was custom-designed for this specific environment with two things in mind. Good results and ease of implementation.
That led me to a **Greedy Heuristic** thinking to optimize and minimize rotations.

> A **greedy heuristic** is an algorithmic strategy that makes a series of locally optimal choices in the hope of finding a global optimum. At each step, it selects the option that appears to be the best or most beneficial at that moment, without reconsidering previous decisions or exploring alternative paths. While this approach is not guaranteed to produce the optimal solution for all problems, it is often used when a quick, reasonably good solution is preferred over a slower, exact one. Greedy heuristics are particularly effective for specific problem types where the locally optimal choice also leads to a globally optimal result.

### Why this works
Explain:
- Stack sizes below 3 are hardcoded
- Each step of the way the algorithm counts which number in **a** has a better rotation count to be pushed to **b** in the correct descending order.
- Then it minimizes rotations by checking if **a** should be rotated alone (`ra rra`) or if it should be rotated with **b** (`rr rrr`)

## 🏗 Architecture

```text
Input Parsing
      ↓
Validation
      ↓
Sorting Engine:
 - Stack size of 2 or 3:
    - Hardcoded
 - Bigger stack:
    - Push top 2 from stack a to stack b
    - Greedy check every nbr in stack a for the better option
    - Greedy check best rotation combination for that nbr combining both a and b
    - Push from a to b
    - Repeat the greedy process until there's only 3 nbrs left in stack a
    - Hardcode sort the 3
    - Push everything from b to a
    - Rotate stack a to minimum value (if needed)
      ↓
Free Allocated Memory
```

## ▶️ Usage

Any of the following
```bash
./push_swap 3 2 5 1 4
./push_swap "3 2 5 1 4"
ARG="3 2 5 1 4"; ./push_swap $ARG
```
Word count the number of steps or use the subject checker
```bash
./push_swap 3 2 5 1 4 | wc -l
./push_swap 3 2 5 1 4 | ./checker_linux 3 2 5 1 4
./push_swap 3 2 5 1 4 | ./checker_Mac 3 2 5 1 4
```
Random tests:
```bash
ARG=$(shuf -i 1-1000 -n 100 | tr '\n' ' '); ./push_swap $ARG | ./checker_linux $ARG
```
## 🧪 Example

```bash
./push_swap 5 1 4 2 3

pb
pb
ra
pa
pa
ra
```

## 📊 Benchmark for 100% ✅

| Input Size | Max Allowed | My Result |
|------------|------------|-----------|
| 100 numbers | < 700 | 524 / 589 |
| 500 numbers | < 5500 | 4812 / 5280 |

The algorithm adapts dynamically based on input distribution to minimize total operations.

## ⚠️ Error Handling

The program must output "Error" to standard error in case of:
- Non-integer arguments
- Integers exceeding allowable int size
- Duplicates
- Incorrect input format

Examples:
```bash
./push_swap 0 1 two 3
Error

./push_swap 1 1
Error
```

## 🔁 Bonus Part — The `checker` Program

### 🧾 Description

A second program named `checker` that validates whether a list of instructions sorts the values properly when applied to the given initial stack state.
`Checker` receives the given list of numbers for stack `a` and then get each of the push_swap instructions in order through the get_next_line function.
Then it compares the results until the end to see if stack `a` is sorted and stack `b` is empty.

### ▶️ Usage
Combine with the `push_swap` on any of the following
```bash
./push_swap 3 2 5 1 4 | ./checker 3 2 5 1 4
./push_swap "3 2 5 1 4" | ./checker "3 2 5 1 4"
ARG="3 2 5 1 4"; ./push_swap $ARG | ./checker $ARG

ARG=$(shuf -i 1-1000 -n 100 | tr '\n' ' '); ./push_swap $ARG | ./checker $ARG

```

## Relevant Repositories
### 🌈 Visualizer
Check this amazing [visualizer](https://github.com/o-reo/push_swap_visualizer) by [Emmanuel Ruaud](https://github.com/o-reo)

100 numbers sort\
![100_sort](/img/100_sort.gif)

500 numbers sort\
![500_sort](/img/500_sort.gif)

## 📁 Project Structure

```text
push_swap/
├── img/
├── includes/
├── libft_printf_gnl/
│   ├── includes/
│   ├── srcs/
│   ├── Makefile
├── srcs/
│   ├── checker/
│   ├── common/
│   ├── push_swap/
├── Makefile
└── README.md
```

## 🎯 Key Learnings

- Time complexity tradeoffs
- Common sorting algorithms
- C array vs list sorting
- Stack-based sorting limitations
- Greedy vs global optimization
- Writing performant C code

## Resources
### On stack data:
https://www.geeksforgeeks.org/c/implement-stack-in-c/
https://www.geeksforgeeks.org/dsa/circular-linked-list/
https://www.youtube.com/watch?v=Flk5yrlx5Qo
https://www.youtube.com/watch?v=YjxKYxpf51E
https://leetcode.fandom.com/wiki/Sort_with_two_stacks
https://www.geeksforgeeks.org/dsa/sorting-a-singly-linked-list/
https://www.geeksforgeeks.org/dsa/sorted-merge-of-two-sorted-doubly-circular-linked-lists/

### On heuristic theory
https://en.wikipedia.org/wiki/Heuristic

### On algorithms
https://en.wikipedia.org/wiki/Stack_(abstract_data_type)
https://42-cursus.gitbook.io/guide/2-rank-02/push_swap/algorithms
https://clementmihailescu.github.io/Sorting-Visualizer/
https://www.youtube.com/watch?v=WprjBK0p6rw
https://www.youtube.com/watch?v=Y95a-8oNqps

### Other
https://www.geeksforgeeks.org/c/how-to-create-typedef-for-function-pointer-in-c/

### 🤖 AI Contributions
- After experimentation and creation of different sorting algorithms, asked for clues on knowledge that could help me know how to check and choose for the optimal way. Lm responded with the Heuristic concept.
- Algorithm comparison.
- List vs array brainstorming.
- 📄 Drafting this README.md in markdown format.
- Debugging Makefile.

## 👨‍💻 Author

Miguel Sobral Curado  
[42 Intra](https://profile.intra.42.fr/users/msobral-) / [GitHub](https://github.com/miguelsobralcurado/)  
[Instagram](https://www.instagram.com/miguelsobralcurado/)

Feel free to contact me with suggestions or improvements!

---

## 🛎️ License

This project is part of the [42 Network](https://www.42network.org/) curriculum.

This project is designed to test your learning and skills.
