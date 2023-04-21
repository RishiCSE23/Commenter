import pandas as pd
import pyfiglet
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=2)


def import_dataset(criteria_file:str, gradebook_file:str) -> dict:
    """_summary_

    Args:
        criteria_file (str): _description_
        gradebook_file (str): _description_

    Returns:
        dict: _description_
    """
    try:
        criteria_df = pd.read_csv(criteria_file)
        gradebook_df = pd.read_csv(gradebook_file)
        result = {'criteria_df':criteria_df, 'gradebook_df':gradebook_df}
    except Exception as e:
        print(str(e))
        result = {}
    finally:
        return result


def generate_dicts(source_df:dict) -> dict:
    """_summary_

    Args:
        source_df (dict): _description_

    Returns:
        dict: _description_
    """
    if not source_df:   # empty dict received
        print('Error: Null dictionary supplied, please check if the file import was correct ')
        return {}  # to suspend processing at the folloing stage 
    else:
        ## convert df to better accessabble dict
        criteria_dict = source_df['criteria_df'].transpose().to_dict()
        students_dict = source_df['gradebook_df'].transpose().to_dict()
    return {'criteria_dict':criteria_dict, 'students_dict':students_dict}


def extract_maps(source_dicts:dict) -> dict:
    """_summary_

    Args:
        source_dicts (dict): _description_

    Raises:
        Exception: _description_

    Returns:
        dict: _description_
    """
    try:
        if not source_dicts:
            raise Exception ('Error: Null dictionary supplied, please check if the file import was correct') 
        
        criteria_dict = source_dicts['criteria_dict']
        students_dict = source_dicts['students_dict']

        criteria_col_map = {}   # maps col names to col index
        student_attr_map = {}  # maps student attributes to col index 

        for col_idx in range(len(criteria_dict)):
            col_name = criteria_dict[col_idx]['Criteria']
            criteria_col_map[col_name] = col_idx

        student_attr_list = list(students_dict[0].keys())
        for i in range(len(student_attr_list)):
            student_attr_map[student_attr_list[i]] = i  

        result = {'criteria_col_map':criteria_col_map, 'student_attr_map':student_attr_map}

    except Exception as e:
        print(str(e))
        result = {}
    
    finally:
        return result


def comment_generator(maps:dict, source_dicts:dict) -> pd.DataFrame:
    """_summary_

    Args:
        maps (dict): _description_
        source_dicts (dict): _description_

    Returns:
        pd.DataFrame: _description_
    """
    students_dict = source_dicts['students_dict']
    criteria_dict = source_dicts['criteria_dict']

    student_comments = {} # maps student_id to {attr : comment}   
    for student_idx in students_dict: 
        student = students_dict[student_idx]  # student of index student_idx
        student_id = students_dict[student_idx]['Student ID']  # get student id  
        
        attr_comment = {}  # maps attr to comment 
        for attr in student:   # iterating all attributes 
            
            if attr != 'Student ID':  # get scores from all atributes but Student ID 
                score = student[attr] # score of an attribute 
                attr_idx = maps['student_attr_map'][attr] -1 # -1 as there's no student id in criteria_dict; 1 index less 
                score_idx = str(score//10)   # in critera dict score are of range [0-10] in str
                comment = criteria_dict[attr_idx][score_idx]
                attr_comment[attr] = comment
        student_comments[student_id] = attr_comment

    return pd.DataFrame(student_comments)

def file_writer(comments_df:pd.DataFrame, filename:str='comments.txt') -> None:
    """_summary_

    Args:
        comments_df (pd.DataFrame): _description_
        filename (str, optional): _description_. Defaults to 'comments.txt'.
    """
    with open(filename, 'a') as fp: 
        for student_id in comments_df.columns.to_list():
            fp.write('------------------------')
            fp.write(f'Student ID:{student_id}' )
            fp.write('------------------------')
            for attr in comments_df[student_id].to_dict():
                fp.write(f'\n {attr} : {comments_df[student_id][attr]}')
            fp.write('\n\n')

def main():
    """
    Process starts here !!
    """
    print(pyfiglet.figlet_format('Welcome to Commenter'))
    prompt = '''
        Welcome to Auto Comment Generator Unitily !!

        In order to run this program correctly, make sure the following are satisfied 
        1. The Gradebook and Criteria file is located at the same folder as the source file 
    '''
    print(prompt)
    criteria_file_name = input('Enter criteria file name: ')
    gradebook_file_name = input('Enter gradebook file name: ')
    output_file_name = input('Enter output file name: ')

    source_df = import_dataset(criteria_file=criteria_file_name, gradebook_file=gradebook_file_name)
    source_dicts = generate_dicts(source_df=source_df)
    maps = extract_maps(source_dicts=source_dicts)
    comments_df = comment_generator(maps=maps, source_dicts=source_dicts)
    file_writer(comments_df=comments_df, filename=output_file_name)

if __name__ == '__main__':
    main()



