def wer(ref: str, hyp: str) -> float:
    r = ref.split(); h = hyp.split()
    dp = [[0]*(len(h)+1) for _ in range(len(r)+1)]
    for i in range(len(r)+1): dp[i][0] = i
    for j in range(len(h)+1): dp[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            cost = 0 if r[i-1] == h[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    return dp[-1][-1] / max(1, len(r))

if __name__ == "__main__":
    print("WER demo:", wer("we will deliver the report tomorrow","we will deliver report tomorrow"))
