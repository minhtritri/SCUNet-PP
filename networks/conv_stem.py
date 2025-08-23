import torch.nn as nn

class ConvStem(nn.Module):
    def __init__(self, in_ch=1, embed_dim=96):
        super().__init__()
        # stride 2 x 2  => tổng giảm 1/4, khớp patch_size=4 mặc định của Swin-UNet
        self.stem = nn.Sequential(
            nn.Conv2d(in_ch, embed_dim // 2, 3, stride=2, padding=1),
            nn.GroupNorm(8, embed_dim // 2), nn.GELU(),
            nn.Conv2d(embed_dim // 2, embed_dim, 3, stride=2, padding=1),
            nn.GroupNorm(8, embed_dim), nn.GELU(),
        )
    def forward(self, x): return self.stem(x)