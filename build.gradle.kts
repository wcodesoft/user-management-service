/*
 * This file was generated by the Gradle 'init' task.
 *
 * This is a general purpose Gradle build.
 * Learn more about Gradle by exploring our samples at https://docs.gradle.org/7.3/samples
 */
allprojects {
    repositories {
        mavenCentral()
        maven("https://plugins.gradle.org/m2/")
        google()
        maven {
            name = "GitHubPackages"
            url = uri("https://maven.pkg.github.com/wcodesoft/user-management-service")
            credentials {
                username = System.getenv("GITHUB_ACTOR")
                password = System.getenv("GITHUB_TOKEN")
            }
        }
    }
}