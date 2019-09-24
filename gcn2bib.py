import urllib.request
from datetime import datetime

bib_template = '''@ARTICLE{GCN%s,
    title = {%s},
    author = {%s and others},
    journal = {GCN},
    volume = {%s},
    pages = {1-+},
    year = {%s}
}

'''

def download_event(event):
    file_name = "%s.gcn3"%event
    url = "https://gcn.gsfc.nasa.gov/other/%s"%file_name
    urllib.request.urlretrieve(url, file_name)
    
def make_bib(event):
    bib_string = ''
    
    filename = event+'.gcn3'
    
    try:
        f = open(filename,'r')
        lines = f.readlines()
        f.close()
    except:
        try:
            f = open(filename,'r', encoding="utf8")
            lines = f.readlines()
            f.close()
        except:
            f = open(filename,'r', encoding="latin-1")
            lines = f.readlines()
            f.close()
            
    circulars = split_circulars(lines)
    
    for circular in circulars:
        gcn_num, gcn_title, gcn_author, gcn_year = get_circular_data(circular)
        bib_entry = bib_template%(gcn_num, gcn_title, gcn_author, gcn_num, gcn_year)
        bib_string += bib_entry
    
    bib_name = event+'.bib'
    bib_file = open(bib_name, 'w')
    bib_file.write(bib_string)
    bib_file.close()
            
    return
    
    
def split_circulars(lines):
    circ_break = '////////////////////////////////////////////////////////////////////////'
    
    circular_list = []
    circ_lines = []
    
    for line in lines[1:]:
        line = line.strip()
        
        if line == circ_break:
            circular_list.append(circ_lines)
            circ_lines = []
        else:
            circ_lines.append(line)
    
    circular_list.append(circ_lines)
            
    return circular_list
    
def get_circular_data(circular):
    gcn_num = circular[1].replace('NUMBER:', '').strip()
    gcn_title = circular[2].replace('SUBJECT:','').strip()
    gcn_date = circular[3].replace('DATE:','').strip()
    
    gcn_datetime = datetime.strptime(gcn_date.replace('GMT','').strip(), '%y/%m/%d %H:%M:%S')
    
    gcn_author = get_author(circular[6])
    
    if gcn_author is False:
        i = 0
        while gcn_author is False:
            gcn_author = get_author(circular[6+i])
            i += 1
        
    gcn_year = gcn_datetime.year
    
    return gcn_num, gcn_title, gcn_author, gcn_year
    
    

def get_author(author_string):
    if author_string.startswith('The IceCube Collaboration') or author_string.startswith('IceCube Collaboration'):
        return 'IceCube Collaboration'
    
    if author_string.startswith('The LIGO Scientific Collaboration'):
        return 'LIGO Scientific Collaboration and Virgo Collaboration'

    if not author_string.split():
        return False
    
    # Most GCNs take the form of Author (Institution), so start with that assumption
    first_author = author_string.split('(')[0]
    
    # Some GCNs list Author1, Author2 ... (Institution), so check that
    if ',' in first_author:
        first_author = first_author.split(',')[0]
   
    # Pull out the last name
    #first_author_lastname = first_author.strip().split()[-1]
    
    if 'LIGO/Virgo' in author_string:
        return False
    
    if 'AUTHORS:' in first_author:
        first_author = first_author.split(':')[-1]
        
    if ',' not in author_string:
        print(author_string)
        print(first_author)
        print()
        
   
    return first_author.strip()#_lastname
   
    
    
if __name__ == '__main__':
    event = 'S190814bv'
    
    download_event(event)
    make_bib(event)
    
    
    
    
