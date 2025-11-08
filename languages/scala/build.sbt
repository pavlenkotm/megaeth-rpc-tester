name := "web3-scala"
version := "1.0.0"
scalaVersion := "2.13.12"

libraryDependencies ++= Seq(
  "org.web3j" % "core" % "4.10.3",
  "org.typelevel" %% "cats-effect" % "3.5.2",
  "org.typelevel" %% "cats-core" % "2.10.0",
  "org.scala-lang.modules" %% "scala-parallel-collections" % "1.0.4"
)
