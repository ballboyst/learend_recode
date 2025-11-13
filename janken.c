#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
	const char* array[] = {"グー","チョキ","パー"};
	int player_choice;
	int cpu_choice;
	int result;

	// 乱数の初期化
	srand((unsigned int)time(NULL));

	// プレイヤーの入力受付
	do {
	printf("あなたは何を出しますか？数字で入力してください\n0:グー\n1:チョキ\n2:パー\n");
	scanf("%d", &player_choice);
	if (player_choice < 0 || player_choice >2) {
	    printf("0から2の数字を入力してください。\n");
	}
} while (player_choice < 0 || player_choice > 2);

// コンピュータの手をランダムに決定
cpu_choice = rand() % 3;

// 結果判定
result = (cpu_choice - player_choice + 3) % 3;

// 出力
printf("あなたは%sを選びました\n", array[player_choice]);
printf("相手は%sでした\n", array[cpu_choice]);

if (result == 0) {
	printf("あいこです\n");
} else if (result == 1) {
	printf("あなたの勝ちです\n");
} else {
	printf("あなたの負けです\n");
}

return 0;
}


