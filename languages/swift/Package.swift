// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "Web3Swift",
    platforms: [
        .macOS(.v12),
        .iOS(.v15)
    ],
    products: [
        .executable(name: "web3client", targets: ["Web3Client"])
    ],
    dependencies: [
        .package(url: "https://github.com/attaswift/BigInt.git", from: "5.3.0"),
    ],
    targets: [
        .executableTarget(
            name: "Web3Client",
            dependencies: ["BigInt"],
            path: "."
        )
    ]
)
