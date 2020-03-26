#include <iostream>

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    unsigned int T;
    std::cin >> T;

    char s[65];
    unsigned long long ans;
    while (T--) {
        std::cin >> s;
        
        ans = 0;
        for (int i = 0; i < 64 && s[i] != '\0'; i++)
            ans = (ans << 1) | (s[i] == '1');

        std::cout << ans << '\n';
    }

    return 0;
}
