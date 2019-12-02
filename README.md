# NER-Spacy
Creating NER model using Spacy amd to get the top 10 rewies of a product.


Intallaion:

    Spacy (For Windows) :
    pip install spacy

    Flask(For Windows) :
    pip install Flask
 
Command to run the script:

    python NerApi.py
    
Output:

  send POST request to http://0.0.0.0:5000/producttags with "text","product_name" as parameters.
  
  sample inputs:
  
    {
      "text":"Asian Gems & Jewels 5 Dhaatu Metal, Alloy Opal Ring - Buy Asian Gems & Jewels 5 Dhaatu Metal, Alloy Opal Men Ring only for          Rs.687 from Flipkart.com. Only Genuine Products. 30 Day Replacement Guarantee. Free Shipping. Cash On Delivery!",
      "product_name":"Wrangle5789r Skande@#$rs Fit9 Men's Jeans"
      }
      
  sample output:
  
    {
    "Category": {
      "Category-1": "Jewellery",
      "Category-2": "Men"
      "Category-3": "Ring"
    },
    "Entities": {
      "ITEMTYPE": [
        "Ring"
      ],
      "MATERIAL": [
        "Men"
      ],
      "METAL": [
        "Alloy"
      ],
      "PRICE": [
        "Rs. 687"
      ]
    },
    "SEO": {
      "KeyWords": [
        "ring  opal  shipping  products  free  day  guarantee  replacement  flipkart"
      ],
      "Meta_Description": [
        "Asian Gems & Jewels 5 Dhaatu Metal, Alloy Opal Ring - Buy Asian Gems & Jewels 5 Dhaatu Metal, Alloy Opal Men Ring only for Rs. 687 from Flipkart.com."
      ],
      "SEO_URL": [
        "Wrangler_Skanders_Fit_Mens_Jeans"
      ]
    }}
  
 send POST request to http://0.0.0.0:5000/reviews and send datafile (Sample data file given in the data folder).
 
  sample Output:


NER- ner model is used to categorize the models.

Reviews- This gives top 10 good and bad reviews of a product.
  
