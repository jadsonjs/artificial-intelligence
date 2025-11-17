package br.com.jadson

import org.apache.commons.csv.CSVFormat
import smile.clustering.KMeans
import smile.data.DataFrame
import smile.data.type.DataTypes
import smile.data.type.StructField
import smile.data.type.StructType
import smile.io.Read

/**
 * The k-means algorithm is an unsupervised machine learning algorithm used for clustering — grouping similar data points
 * into a predefined number of clusters (k). It's widely used for pattern recognition, customer segmentation, image compression, etc.
 *
 *
 */
fun main() {
    try {

        // 1. Load the dataset from CSV file
        val url = object {}.javaClass.getResource("/iris.csv") ?: error("iris.csv not found in resources")
        val path = url.path

        // 2. Define the schema explicitly
        val schema = StructType(
            listOf(
                StructField("sepal.length", DataTypes.DoubleType),
                StructField("sepal.width", DataTypes.DoubleType),
                StructField("petal.length", DataTypes.DoubleType),
                StructField("petal.width", DataTypes.DoubleType),
                StructField("variety", DataTypes.StringType)
            )
        )

        val format = CSVFormat.Builder.create(CSVFormat.DEFAULT)
            .setHeader()
            .setDelimiter(',')
            .setQuote('"')
            .setIgnoreSurroundingSpaces(true)
            .build()

        val iris: DataFrame =  Read.csv(path, format, schema)

        // 2. Remove the "species" column (labels) and use only feature columns
        val features: Array<DoubleArray> = iris.drop("variety").toArray()


        // 3. Define the number of clusters (we know there are 3 species in Iris dataset)
        val k = 3

        // 4. Run K-Means clustering
        val model = KMeans.fit(features, k)

        // 5. Print cluster assignments
        println("Clusters:")
        model.y.forEachIndexed { index, cluster ->
            println("Sample $index -> Cluster $cluster")
        }

        // 6. Print distortion (average squared error within clusters)
        // Lower distortion means points are closer to their cluster centers → better compactness, likely better clustering.
        //Higher distortion means points are more spread out from their centers → less compact clusters.
        println("Distortion: ${model.distortion}")

    } catch (e: Exception) {
        e.printStackTrace()
    }
}