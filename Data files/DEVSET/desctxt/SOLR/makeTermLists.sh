echo "Generating data for the dev set"
./makeTermList.sh me2014_devset_userdoc devset_textTermsPerUser.txt
./makeTermList.sh me2014_devset_imagedoc devset_textTermsPerImage.txt
./makeTermList.sh me2014_devset_POIdoc devset_textTermsPerPOI.txt

echo "Generating data for the test set"
./makeTermList.sh me2014_testset_userdoc testset_textTermsPerUser.txt
./makeTermList.sh me2014_testset_imagedoc testset_textTermsPerImage.txt
./makeTermList.sh me2014_testset_POIdoc testset_textTermsPerPOI.txt

echo "Generating data for both dev and test sets together"
./makeTermList.sh me2014_all_userdoc all_textTermsPerUser.txt
./makeTermList.sh me2014_all_imagedoc all_textTermsPerImage.txt
./makeTermList.sh me2014_all_POIdoc all_textTermsPerPOI.txt
