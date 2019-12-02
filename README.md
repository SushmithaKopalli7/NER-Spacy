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
  
 send POST request to http://0.0.0.0:5000/reviews and send datafile (download sample data file from                                      https://www.kaggle.com/jiashenliu/515k-hotel-reviews-data-in-europe).
 
  sample Output:
  
                                                     review    pos
        43101    A perfect location comfortable great value  0.931
        211742               Clean comfortable lovely staff  0.907
        175551            Friendly welcome Comfortable room  0.905
        365085                    Good location great value  0.904
        109564               Clean friendly and comfortable  0.902
        145743                  Good value amazing location  0.901
        407590            breakfast excellent Clean comfort  0.899
        407546                       Great place I enjoyed   0.881
        218571                Beautiful Quirky Comfortable   0.878
        436901                    Lovely comfortable rooms   0.877


NER- ner model is used to categorize the models.

Reviews- This gives top 10 good and bad reviews of a product.
  
