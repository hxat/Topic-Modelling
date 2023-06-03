from wordcloud import WordCloud,ImageColorGenerator
from PIL import Image
import numpy as np
import pandas as pd

def wordcloud(cluster: int):
    """
        Generates a wordcloud image based on a given text, using a mask in the shape of the Twitter logo.
        Note that this docstring assumes that the Twitter logo is used as a mask for the wordcloud, as suggested by the use of `http://clipart-library.com/image_gallery2/Twitter-PNG-Image.png` in the code. 
        If a different mask is used, the docstring may need to be modified accordingly.

        Args:
            cluster (str): the text to generate the wordcloud from.
            
        Returns:
            None
            
        Prints:
            A wordcloud image, generated using the WordCloud function from the wordcloud library, and overlaid with the color of the Twitter logo.
    """

    # combining the image with the dataset
    Mask = np.array(Image.open(requests.get('http://clipart-library.com/image_gallery2/Twitter-PNG-Image.png', stream=True).raw))

    # We use the ImageColorGenerator library from Wordcloud 
    # Here we take the color of the image and impose it over our wordcloud
    image_colors = ImageColorGenerator(Mask)
    # generate wordcloud
    wc = WordCloud(background_color='white', height=1500, width=4000,mask=Mask).generate(cluster)
    # plot the image
    plt.figure(figsize=(10,20))
    plt.imshow(wc.recolor(color_func=image_colors),interpolation="hamming")
    # plt.axis('off')
    plt.show()



def identify_topics(df: pd.DataFrame, desc_matrix: np.array, num_clusters: int):
    """
        Runs k-means clustering on a matrix of tweet descriptions, and generates a wordcloud for each of the resulting clusters.
    Args:
        num_clusters (int): the desired number of clusters for the k-means algorithm.
        desc_matrix (numpy.ndarray): a matrix of tweet descriptions, where each row corresponds to a single tweet and each column contains a feature of the tweet.
        df (pandas.DataFrame): a DataFrame containing a column of cleaned tweet texts.
    Prints:
        The frequency of tweets in each cluster, as determined by the k-means algorithm.
    Generates:
        A wordcloud for each cluster, showing the most frequently occurring words in the tweets belonging to the cluster.
    """
    km = KMeans(n_clusters=num_clusters)
    km.fit(desc_matrix)
    clusters = km.labels_.tolist()
    tweets = {'Tweet': df["Clean_text"].tolist(), 'Cluster': clusters}
    frame = pd.DataFrame(tweets, index = [clusters])
    print(frame['Cluster'].value_counts()) 
    for cluster in range(num_clusters):
        cluster_words = ' '.join(text for text in frame[frame['Cluster'] == cluster]['Tweet'])
        wordcloud(cluster_words)