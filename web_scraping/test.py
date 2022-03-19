import course

def test_course():
  math241 = Course("spring", "2022", "MATH241")
  try:
      math241.subject == "MATH"
  except:
      print("bad subject")
      raise ValueError
            
  try:
      math241.num == "241"
  except:
      print("bad num")
      raise ValueError
  
  try:
      math241.sections['ADB']
  except:
      print("bad sections")
      raise ValueError
  
  test_section(math241.sections['ADB'])

def test_section(s):
  try:
    s.course == "MATH"
  except:
    print("bad subject")
    raise ValueError
            
  try:
    s.name == "ADB"
  except:
    print("bad name")
    raise ValueError
  
  try:
    s.section_type == "Discussion/Recitation"
  except:
    print("bad type")
    raise ValueError
            
  try:
    s.section_type == "Altgeld Hall"
  except:
    print("bad location")
    raise ValueError
  try:
    s.days == "TR"
  except:
    print("bad days")
    raise ValueError
   
test_course()
