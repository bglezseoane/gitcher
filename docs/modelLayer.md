# gitcher model layer

The gitcher profiles will be saved into a $HOME's dotfile named `.cherfile`.

Using the gitcher options it's easier to add new profiles and it's the recommended method to do. Manually modifying the file has the disappointment that it is possible to add the new profiles incorrectly due to typing errors.


## Format

File data rows are composed by:

`profName, name, email, signKey, signPref`

The `profName` parameter acts like primary key of the dataset and have to be unique. Comma (`,`) acts as separator, so quotation marks are not needed to enclose parameters of more than one word.

