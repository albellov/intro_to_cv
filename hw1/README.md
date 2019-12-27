## Goal: build a CV algorithm to solve Sudoku 

**Part 1: Normalize the image**

- Step 1: find some keypoints (see the helper)
- Step 2: apply ProjectiveTransform (see the notebook from lecture 3)

**Part 2: Recognize digits**
Step 3: manually create templates using normalized images
Step 4: apply match_template (Links to an external site.) to estimate correlation with your templates.
Step 5: make a decision for each cell.
Part 3: solve sudoku using solve_sudoku from sudoku.py

 

## Grading

**Part 1: Normalize the image**

- 5 points: if your pipeline works on a training image in your notebook
- 5 points: testing by TA after the submission using 5 test images. 1 point for each valid result.
- +2 bonus point. The same as 2 but with tricky images.

**Part 2: Recognize digits.**
The same as 1. An image is counted as recognized if you have 3 or fewer errors out of 81 sudoku cells.

- 5 points: if your pipeline works on a training image in your notebook
- 5 points: testing by TA after the submission using 5 test images. 1 point for each valid result.
- +2 bonus point. The same as 2 but with tricky images.

**Part 3: Solve sudoku.**

- +3 bonus point if you have the complete algorithm to solve sudoku & code to display the result on the original image. This part will be validated in your notebook.

