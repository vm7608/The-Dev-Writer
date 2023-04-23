from post_app.models import Topic

topic1 = Topic(name='Algorithm')
topic2 = Topic(name='Database')
topic3 = Topic(name='Machine Learning')
topic4 = Topic(name='Data Science')
topic5 = Topic(name='Web Development')
topic6 = Topic(name='Else')


topic_list = [topic1, topic2, topic3, topic4, topic5, topic6]
for topic in topic_list:
    topic.save()
