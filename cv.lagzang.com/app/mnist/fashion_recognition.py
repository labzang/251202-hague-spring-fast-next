# Fashion-MNIST(패션 의류 인식) 문제를 신경망으로 풀어봅니다.
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np
import os


class FashionMnistTest:
    def __init__(self):
        self.class_names = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot",
        ]

    def create_model(self):
        # 데이터 디렉토리 경로 설정
        data_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "fashion-mnist"
        )

        # Fashion-MNIST 데이터를 다운로드하고 로드합니다.
        # transforms.ToTensor()는 이미지를 텐서로 변환하고, 0~255 값을 0~1로 정규화합니다.
        transform = transforms.Compose([transforms.ToTensor()])

        train_dataset = datasets.FashionMNIST(
            root=data_dir, train=True, download=True, transform=transform
        )

        test_dataset = datasets.FashionMNIST(
            root=data_dir, train=False, download=True, transform=transform
        )

        # 데이터 로더 생성
        batch_size = 100
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        # 데이터 시각화 (25개 샘플)
        self._visualize_samples(train_dataset, train_loader)

        # 모델 생성
        model = FashionNet()

        # 손실 함수와 최적화 함수 설정
        criterion = nn.CrossEntropyLoss()  # sparse_categorical_crossentropy와 동일
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        # 학습
        model.train()
        num_epochs = 5
        total_batch = len(train_loader)

        for epoch in range(num_epochs):
            running_loss = 0.0
            for images, labels in train_loader:
                # 그래디언트 초기화
                optimizer.zero_grad()

                # 순전파: 모델에 입력 데이터를 전달하여 예측값 계산
                outputs = model(images)

                # 손실 계산
                loss = criterion(outputs, labels)

                # 역전파: 그래디언트 계산
                loss.backward()

                # 가중치 업데이트
                optimizer.step()

                running_loss += loss.item()

            print(
                f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / total_batch:.4f}"
            )

        print("\n학습 완료!")

        # 테스트
        test_loss, test_acc = self._evaluate_model(model, test_loader, criterion)
        print(f"\n테스트 정확도: {test_acc:.4f}")

        # 예측
        predictions, test_images, test_labels = self._predict(model, test_loader)

        print(f"\n예측 결과 샘플 (인덱스 3): {predictions[3]}")

        # 10개 클래스에 대한 예측을 그래프화
        arr = [predictions, test_labels, test_images]
        return arr

    def _visualize_samples(self, train_dataset, train_loader):
        """학습 데이터 샘플 25개 시각화"""
        # 데이터셋에서 25개 샘플 가져오기
        fig, axes = plt.subplots(5, 5, figsize=(10, 10))
        for i in range(25):
            image, label = train_dataset[i]
            row, col = i // 5, i % 5
            axes[row, col].imshow(image.squeeze(), cmap=plt.cm.binary)
            axes[row, col].set_title(self.class_names[label])
            axes[row, col].axis("off")
        plt.tight_layout()
        # plt.show()  # 주석 처리 (필요시 활성화)

    def _evaluate_model(self, model, test_loader, criterion):
        """모델 평가"""
        model.eval()
        test_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                loss = criterion(outputs, labels)
                test_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        accuracy = 100 * correct / total
        avg_loss = test_loss / len(test_loader)
        return avg_loss, accuracy

    def _predict(self, model, test_loader):
        """모델 예측"""
        model.eval()
        all_predictions = []
        all_images = []
        all_labels = []

        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                # softmax 적용하여 확률값으로 변환
                probabilities = F.softmax(outputs, dim=1)

                all_predictions.extend(probabilities.cpu().numpy())
                all_images.extend(images.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

        return np.array(all_predictions), np.array(all_images), np.array(all_labels)

    def plot_image(self, i, predictions_array, true_label, img):
        """단일 이미지와 예측 결과 시각화"""
        print(" === plot_image 로 진입 ===")
        predictions_array, true_label, img = (
            predictions_array[i],
            true_label[i],
            img[i],
        )
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])

        # 이미지가 (1, 28, 28) 형태이면 squeeze
        if len(img.shape) == 3 and img.shape[0] == 1:
            img = img.squeeze()

        plt.imshow(img, cmap=plt.cm.binary)
        # plt.show()  # 주석 처리 (필요시 활성화)

        predicted_label = np.argmax(predictions_array)
        if predicted_label == true_label:
            color = "blue"
        else:
            color = "red"

        plt.xlabel(
            "{} {:2.0f}% ({})".format(
                self.class_names[predicted_label],
                100 * np.max(predictions_array),
                self.class_names[true_label],
            ),
            color=color,
        )

    @staticmethod
    def plot_value_array(i, predictions_array, true_label):
        """예측 확률값을 막대 그래프로 시각화"""
        predictions_array, true_label = (
            predictions_array[i],
            true_label[i],
        )
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        thisplot = plt.bar(range(10), predictions_array, color="#777777")
        plt.ylim([0, 1])
        predicted_label = np.argmax(predictions_array)

        thisplot[predicted_label].set_color("red")
        thisplot[true_label].set_color("blue")


class FashionNet(nn.Module):
    """
    Fashion-MNIST 분류를 위한 신경망 모델
    relu (Rectified Linear Unit 정류한 선형 유닛)
    미분 가능한 0과 1사이의 값을 갖도록 하는 알고리즘
    softmax
    nn (neural network)의 최상위층에서 사용되며 classification을 위한 function
    결과를 확률값으로 해석하기 위한 알고리즘
    """

    def __init__(self):
        super(FashionNet, self).__init__()
        # Flatten: (28, 28) -> 784
        self.flatten = nn.Flatten()
        # Dense(128, activation='relu')
        self.fc1 = nn.Linear(28 * 28, 128)
        # Dense(10, activation='softmax')
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # Flatten: 입력 이미지를 1차원 벡터로 변환
        x = self.flatten(x)
        # 첫 번째 레이어: ReLU 활성화 함수 적용
        x = F.relu(self.fc1(x))
        # 두 번째 레이어: 출력 레이어 (softmax는 손실 함수에서 처리되거나 별도로 적용)
        x = self.fc2(x)
        return x


if __name__ == "__main__":
    # Fashion-MNIST 테스트 객체 생성
    fashion_test = FashionMnistTest()

    # 모델 생성, 학습, 평가, 예측
    arr = fashion_test.create_model()

    # 예측 결과, 테스트 레이블, 테스트 이미지
    predictions, test_labels, test_images = arr

    # 예시: 첫 번째 이미지 시각화
    # fashion_test.plot_image(0, predictions, test_labels, test_images)
    # FashionMnistTest.plot_value_array(0, predictions, test_labels)
    # plt.show()  # 주석 처리 (필요시 활성화)
