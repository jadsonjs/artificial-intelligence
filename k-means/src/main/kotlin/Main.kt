package br.com.jadson

import smile.clustering.KMeans
import smile.data.DataFrame
import smile.io.Read

fun main() {
    try {
        // 1. Load the dataset from CSV file
        val iris: DataFrame = Read.csv("src/main/resources/iris.csv")

        // 2. Remove the "species" column (labels) and use only feature columns
        val features: Array<DoubleArray> = iris.drop("species").toArray()

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
        println("Distortion: ${model.distortion}")
    } catch (e: Exception) {
        e.printStackTrace()
    }
}