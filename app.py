from usellm import Message, Options, UseLLM
import json
from flask import Flask, render_template, request

# Initialize the service
service = UseLLM(service_url="https://usellm.org/api/llm")


################################### Generate Summary ###################################
def get_summary(article_url):

	system_property= '''You are a bot that helps summarizing news articles in an accurate and concise manner. 

	The user will give you the link to the news article, and upon analysis, you must generate an output of the news article that is strictly under 100 words for a summary, a headline under 10 words, and an image prompt based on the emotion, background, setting, and purpose of the article. 

	Your output should be presented in the form of a JSON string: {"Summary": {{ summary }}, "Headline": {{ headline }}, "Image prompt": {{ image_prompt}}}.

	Your output should be accurate and should reflect the original content of the news article. If you are unhappy with your results, do not hesitate to iterate and refine it'''

	assistant_example_op='''{"Summary": "Deepak Chahar's exceptional performance in the IPL has garnered praise as he skillfully neutralized experienced players like Shubman Gill. Captain MS Dhoni also commended his outstanding displays, elevating Chahar's recognition in recent weeks.", "Headline": "Deepak Chahar's Impressive IPL Performance Earns Praise and Recognition", "Image prompt":  "News article picture of the talented bowler with yellow jersey number 90 bowling in a cricket stadium full of audience 300mm lens professional photography rear side"}'''
	# Prepare the conversation
	messages = [
	Message(role="system", content=system_property),
	Message(role="user", content="https://indianexpress.com/article/sports/ipl/the-shubman-gill-nullifier-what-makes-deepak-chahar-ms-dhonis-favorite-8632304/"),
	Message(role="assistant", content=assistant_example_op),
	Message(role="user", content=article_url),
	]
	options = Options(messages=messages)

	# Interact with the service
	response = service.chat(options)

	# Print the assistant's response
	print("Chat response ::: {}\n\n".format(response.content))

	data = json.loads(response.content)

	# image_prompt = data["Image prompt"]

	# print("Image promt is ::: {}".format(image_prompt))

	return dict(data)

def get_better_image_prompt(noob_image_prompt):
	system_property= '''You're an illustration artist who posses mixed skills of the best  James Gurney, Craig Mullins, Lois van Baarle (Loish), and Rebecca Mock. 

The user will give you an image prompt and you need to return a better image prompt depicting the same image. 

Free to include settings from the list in the prompt that best suits the situation but not more than 3: [digital illustration, 4k resolution, 8k resolution, detailed background,  fantasy vivid colors]

Return the output in JSON format: {"Image prompt": {{ image_prompt }}}'''

	assistant_example_op='''{"Image prompt": "A portrait of Erdogan addressing a grandiose gathering of cheering supporters amidst a sea of fluttering Turkish flags, 4k resolution"}'''
	# Prepare the conversation
	messages = [
	Message(role="system", content=system_property),
	Message(role="user", content="A picture of Erdogan addressing an audience of ardent supports waving Turkey's flag"),
	Message(role="assistant", content=assistant_example_op),
	Message(role="user", content=noob_image_prompt),
	]
	options = Options(messages=messages)

	# Interact with the service
	response = service.chat(options)

	# Print the assistant's response
	print("Chat response ::: {}\n\n".format(response.content))

	data = json.loads(response.content)

	# image_prompt = data["Image prompt"]

	# print("Image promt is ::: {}".format(image_prompt))

	return dict(data)
################################################################################

######################### Generate Image ########################################

def get_image(image_prompt):
	# image_prompt = "A picture of Turkish President Erdogan during a political rally standing on a stage with a microphone in front of a large crowd in a colorful political background"
	image_options = Options(prompt=image_prompt)

	response = service.generate_image(image_options)

	url=response.images[0]
	# print(response.images[0])
	# image_path = urllib.request.urlopen(url)
	# logo = Image.open(image_path)
	return url


app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def show_img():
	if request.method == "POST":
		article_info = request.form["output"]
		summary_data = get_summary(article_info)
		print("summary_data, Datatype: {}, Value: {}".format(type(summary_data), summary_data))
		prompt_data = get_better_image_prompt(summary_data["Image prompt"])
		print("prompt_data, Datatype: {}, Value: {}".format(type(prompt_data), prompt_data))
		image_prompt = prompt_data["Image prompt"]
		print("Image, Datatype: {}, Value: {}".format(type(image_prompt), image_prompt))
		article_summary = summary_data["Summary"]
		print("article_summary, Datatype: {}, Value: {}".format(type(article_summary), article_summary))
		article_headline = summary_data["Headline"]
		print("article_headline, Datatype: {}, Value: {}".format(type(article_headline), article_headline))
		image_url = get_image(image_prompt)
		return render_template('index.html', url=image_url, headline=article_headline, summary=article_summary)
	else:
		return render_template('index.html', url="https://via.placeholder.com/400", headline="Submit your article")
