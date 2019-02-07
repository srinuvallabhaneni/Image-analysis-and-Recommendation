# Image-analysis-and-Recommendation

How to run

pip install -r requirements.txt
python main.py
How to use Run “python main.py” Menu Options:

Task 1 2a. Task 2a 2b. Task 2b
Task 3
Task 4 5a. Task 5a 5b. Task 5b RUN 5a before this to build index structure 6a. Task 6a With k 6aa Task 6aa without k 6b. Task 6b
Load data
Quit
Please run task 8 - load data before executing any file - This is a one time process for every system.

Once the data loading is done and the mongodb is up and running:

As all tasks are dependent on task 1, make sure to run task 1 after data loading is done before running any task.
Then, execute any task as needed according to the instructions on the screen.
Task 1: Implement a program which, given a value k, creates an image-image similarity graph, such that from each image, there are k outgoing edges to k most similar/related images to it.

Task 2: Given the image-image graph, identify c clusters (for a user supplied c) using two distinct algorithms. You can use the graph partitioning/clustering algorithms of your choice for this task. Visualize the resulting image clusters.

Task 3: Given an image-image graph, identify and visualize K most dominant images using Page Rank (PR) for a user supplied K.

Task 4: Given an image-image graph and 3 user specified imageids identify and visualize K most relevant images using personalized PageRank (PPR) for a user supplied K.

Task 5: – 5a:ImplementaLocalitySensitiveHashing(LSH)tool,foraandsimilarity/distancefunctionofyourchoice,which takes as input (a) the number of layers, L, (b) the number of hashes per layer, k, and (c) a set of vectors as input and creates an in-memory index structure containing the given set of vectors.

– 5b: Implement similar image search using this index structure and a combined visual model function of your choice (the combined visual model must have at least 256 dimensions): for a given image and t, visulizes the t most similar images (also outputs the numbers of unique and overall number of images considered).

Task 6: Implement • a k-nearest neighbor based classification algorithm, and • a PPR-based classification algorithm which take a file containing a set of image/label pairs and associates a label to the rest of the images in the database. Visualize the labeled results.
