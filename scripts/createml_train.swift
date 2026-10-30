// Train and test an image classifier with Apple's Create ML engine (the same engine as the Create ML app).
// usage: swift createml_train.swift <dataset_dir_with_train_val_test> <out.mlmodel>
import CreateML
import Foundation

let args = CommandLine.arguments
let root = URL(fileURLWithPath: args[1])
let start = Date()
let params = MLImageClassifier.ModelParameters(
    validation: .dataSource(.labeledDirectories(at: root.appendingPathComponent("val"))),
    maxIterations: 25)
let model = try MLImageClassifier(trainingData: .labeledDirectories(at: root.appendingPathComponent("train")),
                                  parameters: params)
let secs = Date().timeIntervalSince(start)
let trainAcc = 1 - model.trainingMetrics.classificationError
let valAcc = 1 - model.validationMetrics.classificationError
let test = model.evaluation(on: .labeledDirectories(at: root.appendingPathComponent("test")))
print(String(format: "train %.3f  val %.3f  test %.3f  time %.0f s", trainAcc, valAcc, 1 - test.classificationError, secs))
print(test.confusion)
try model.write(to: URL(fileURLWithPath: args[2]))
