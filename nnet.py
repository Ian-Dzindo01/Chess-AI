from torch.utils.data import Dataset
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
from timeit import default_timer as timer


class ChessValueDataset(Dataset):
    def __init__(self):
        dat = np.load("D:/Projects/AI/Chess AI/processed/dataset_500K.npz")
        self.X = dat['arr_0']
        self.Y = dat['arr_1']
        print(self.X.shape)
        print(self.Y.shape)

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return (self.X[idx], self.Y[idx])


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.a1 = nn.Conv2d(5, 16, kernel_size=3, padding=1)           # in-channels, out-channels, kernel size
        self.a2 = nn.Conv2d(16, 16, kernel_size=3, padding=1)
        self.a3 = nn.Conv2d(16, 32, kernel_size=3, stride=2)

        self.b1 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.b2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.b3 = nn.Conv2d(32, 64, kernel_size=3, stride=2)

        self.c1 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.c2 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.c3 = nn.Conv2d(64, 128, kernel_size=2, stride=2)

        self.d1 = nn.Conv2d(128, 128, kernel_size=1)
        self.d2 = nn.Conv2d(128, 128, kernel_size=1)
        self.d3 = nn.Conv2d(128, 128, kernel_size=1)

        self.last = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.a1(x))               # RELU is used instead of the sigmoid function to squishify the activations on each neuron.
        x = F.relu(self.a2(x))
        x = F.relu(self.a3(x))

        # 4x4
        x = F.relu(self.b1(x))
        x = F.relu(self.b2(x))
        x = F.relu(self.b3(x))

        # 2x2
        x = F.relu(self.c1(x))
        x = F.relu(self.c2(x))
        x = F.relu(self.c3(x))

        # 1x128
        x = F.relu(self.d1(x))
        x = F.relu(self.d2(x))
        x = F.relu(self.d3(x))

        x = x.view(-1, 128)
        x = self.last(x)

        # value output
        return torch.tanh(x)


if __name__ == '__main__':

    start0 = timer()
    device = "cpu"
    chess_dataset = ChessValueDataset()
    train_loader = torch.utils.data.DataLoader(chess_dataset, batch_size=256, shuffle=True)   # loads the training data.
    model = Net()
    optimizer = optim.Adam(model.parameters())                  # optimizer used to find local minimums, I guess.
    floss = nn.MSELoss()     # loss function that is to be minimized

    model.train()

    for epoch in range(100):
        all_loss = 0
        num_loss = 0
        start1 = timer()
        for batch_idx, (data, target) in enumerate(train_loader):
            target = target.unsqueeze(-1)
            data, target = data.to(device), target.to(device)       # Sends the data and target to the cpu
            data = data.float()
            target = target.float()

            # print(data.shape, target.shape)
            optimizer.zero_grad()                                   # Clears the gradients of all optimized torch.Tensor s?.
            output = model(data)
            # print(output.shape)

            loss = floss(output, target)                       # Backpropagation here. This calculates the loss function.
            loss.backward()
            optimizer.step()

            all_loss += loss.item()
            num_loss += 1

        print(f'{epoch}. Loss: {all_loss/num_loss}, Time took: {timer() - start1}')
        torch.save(model.state_dict(), "nets/value5M.pth")

    print(f'The training took: {(timer() - start0)/3600}')
