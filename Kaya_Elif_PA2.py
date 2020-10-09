'''
Created on Jan 25, 2020

@author: elif
'''


def fromFile(file):
    file = open(file, 'r')
    line = file.read() 
    return line 

txtfile = input("Please enter the name of the file containing the text: ")
print()
textOrig = fromFile(txtfile)
text_duplicate = textOrig.lower()
print('Contents of file',txtfile)
print (textOrig)

# your code goes here
print()
keyword = input('Enter the keyword: ').lower()

#We replace the new line character with spaces
clean_text = text_duplicate.replace("\n", " ")

#replace different punctuation with just "."
text_w_period = clean_text.replace('?', '.').replace('!', '.')

#Replace all the punctuation with space only 
text_w_space = text_w_period.replace(',', '.').replace(':', '.').replace(';', '.').replace('-', '.')\
 .replace('"', '.').replace("'", '.').replace('.', ' ')

#Getting the position of the input value
first_pos =  (" "+text_w_space+" ").find(" "+ keyword+" ")

#Getting the total length of the text 
text_length = len(text_duplicate)
   

#Creating the if statement to find the input value in the text else print it does not appear in text
if first_pos > -1:

        
    #Getting the line length from the user
    line_length = eval(input("Enter the line length: "))
    print("----------")
        

    #Finding the "." before and after our keyword's index number    
    beg_of_sentence  = text_w_period.rfind(".",0, first_pos)
    end_of_sentence = text_w_period.find(".", first_pos)
        
    #Making a full sentence including our keyword 
    sentence = textOrig[beg_of_sentence +1: end_of_sentence+1]
    
    #Finding the new position of our keyword in the sentence containing the keyword
    new_pos = first_pos - beg_of_sentence - 1
    final_sentence = sentence[:new_pos ]+ keyword.upper()+ sentence[new_pos + len(keyword):]
    print("Outputting the sentence followed by the text schema with", line_length, "characters per line:")
    print("*****")
    print(final_sentence.strip().replace("\n", " "))
    

    #Schematic representation of the text
    total_lines = text_length // line_length #Finding the total lines we need to display the schema
    last_line_length = text_length % line_length 
    
    #Create schema with only dots.
    schema = ['.'*line_length]*total_lines
    schema.append('.'*last_line_length)
    
    #Replace dots with keyword
    line_w_keyword = first_pos // line_length
    actual_sentence = schema[line_w_keyword]
    part1 = actual_sentence [:first_pos %line_length]
    part2 = keyword.upper()
    part3 = actual_sentence[first_pos%line_length + len(keyword):]
    new_line = part1 + part2 + part3
    
    #Multiline keyword
    if len(new_line) > line_length:
        extra = new_line[line_length:]

        new_line = new_line[:line_length]
        remaining_word = (line_length - len(extra)) * "."
        schema[line_w_keyword + 1] = extra + remaining_word
   
    schema[line_w_keyword] = new_line
    print("\n".join(schema))

else:
    print('"{}"'.format(keyword),"does not appear in the text")
