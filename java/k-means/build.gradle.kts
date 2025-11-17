plugins {
    kotlin("jvm") version "2.0.21"
}

group = "br.com.jadson"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    // Smile - Statistical Machine Intelligence and Learning Engine
    implementation("com.github.haifengl:smile-core:3.0.0")

    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}
kotlin {
    jvmToolchain(21)
}