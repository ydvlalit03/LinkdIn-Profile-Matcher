import json
from script import fields, prepare_query, sum , weight_of_image_if_negative , weight_of_image_if_positive, search_linkedin_profiles_selenium
from script import model, LinkedInProvider, transform_data, calculate_similarity, safe_text, scores


# Step 1: Import JSON data file
with open('/Users/manaspatil/Desktop/NLP/dataset2.json', 'r') as file:
    data = json.load(file)

# Step 2: Process each instance and store in 'query'
query = []

for person in data:
    query.append(person)

# Make a answer dictionary to store the final answer (i.e person's most probable LinkedIn profile and the associated 
# confidence level)
answer=dict()

# Step 5: Processes every persona

for person in query:

  # Use prepare_query function from scipt module to make a search string
  search = prepare_query(person)
  print(person)

  # Fetch possible LinkedIn profiles
  links = search_linkedin_profiles_selenium(search, max_results=5)
  print(links)

  # Make the vector embeddings of our persona (given in data.json)
  encoded_profile1 = {field: model.encode(safe_text(person[field])) for field in fields}
  confidence_score=0.0
  profile=str()

  # For each LinkedIn profile, fetch the LinkedIn data using scrapper and then make the vector embedding for them too
  for link in links:
    result = LinkedInProvider().person_profile(link)
    i=0
    while result is None and i<=5:
      i+=1
      result = LinkedInProvider().person_profile(link)
    if(result==None):
      print(f"Cannot fetch linkedIn for profile: {link}")
      continue
    data = result[0]
    complete_data = result[1]
    transformed_data = transform_data(data , complete_data)

    encoded_profile2 = {field: model.encode(safe_text(transformed_data[field])) for field in fields}
    sum,score=scores(fields,encoded_profile1,encoded_profile2,person)

    # Now compare the images (if not NULL) with the given image (if not NULL)
    # Here sum is the current sum of weights which will be used to later normalise the score to get the final confidence score
    url1 = person['image']
    url2 = transformed_data['image']
    if(url1!=None and url2!=None):
      try :
        similarity=calculate_similarity(url1, url2)
      except :
        similarity = 0
      if(similarity>0.4):
        sum+=weight_of_image_if_positive
        score+=weight_of_image_if_positive*similarity
      elif(similarity!=0):
        sum+=weight_of_image_if_negative
        score+=weight_of_image_if_negative*similarity
    # Select the profile with maximum condidence score
    if(confidence_score<score/sum):
      confidence_score=score/sum
      profile=link
    print(f"Score for profile {link}: ",score/sum)
  print(f"Person Profile: {profile} and Confidence Score: {confidence_score}")
  answer[person['name']]=[profile,confidence_score]

  # Print the final answer
  for k in answer:
    print(f"{k}:\nPerson Profile: {answer[k][0]} and Confidence Score: {answer[k][1]}")