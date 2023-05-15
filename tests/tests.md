integration tests:
file retrieval - 
1. Verify the correct number of files is returned
2. Ensure that the expected files are included in the list
3. Validate that the file names are correctly extracted

invoice regex - 
1. Verify that the invoice numbers are correctly extracted for different file name formats.
2. Ensure that the script handles variations of invoice number formats gracefully.

pdf combine - 
Create a set of test PDF files with the same invoice number and different contents
1. Verify that the script correctly combines these PDFs into a single PDF file
2. Ensure that all the combined pages are included in the combined PDF

file saving - 
1. Comfirm that the script creates the specified directory if it doesnt exist
2. Verify that teh combined PDF file is saved into the correct location
3. Ensure that the script handles file naming conflicts (ie when a file with the same name already exists)

error handling - 
simulate the designated folder not existing and verify that the script handles the scenario gracefully
1. Test scenaiors where the script encounters inaccessbile files or permissions issues

overall functionality - 
1. Create a mock test environment with a set of test files in the designated folder
2. Run the script and verify that the correct files are moved, combined, and saved as expected

performance - 
1. Measure the execution time of the script for different file sizes and quantities
2. Verify that the script performs within acceptable time limits of requirements

behavior - 
1. Test the behavior of the script when no files or invoices are found in the folder

error and info logging -
1. Verify that the error logs are generated and contain relevant information
2. Ensure that error notifications or reports are sent or displayed appropriately