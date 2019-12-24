/*
 * Program that solves a small linear equation with Cramer's Rule.
 */

#include <cmath>
#include <iostream>
#include <map>
#include <vector>

typedef long double fat_boi;
typedef std::vector<std::vector<fat_boi> > matrix;

std::map<matrix, fat_boi> cache;


fat_boi get_determinant(const matrix &input_matrix, const size_t &size);

fat_boi get_determinant1(const matrix &input_matrix);

fat_boi get_determinant2(const matrix &input_matrix);

fat_boi get_determinant3(const matrix &input_matrix);

matrix replace_column(
        matrix input_matrix,
        const size_t &size,
        const size_t &replace_column,
        const std::vector<fat_boi> &replace_values);

matrix shrink_matrix(
        const matrix &input_matrix,
        const size_t &size,
        const size_t &remove_row,
        const size_t &remove_column);


int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);

    size_t N;
    std::cin >> N;

    matrix input_matrix(N, std::vector<fat_boi>(N, 0));
    for (size_t row_i = 0; row_i < N; row_i++) {
        for (size_t col_i = 0; col_i < N; col_i++) {
            std::cin >> input_matrix[row_i][col_i];
        }
    }

    std::vector<fat_boi> y_matrix(N, 0);
    for (size_t i = 0; i < N; i++) {
        std::cin >> y_matrix[i];
    }

    fat_boi original_determinant = get_determinant(input_matrix, N);
    std::vector<fat_boi> solved_matrix(N, 0);
    for (size_t i = 0; i < N; i++) {
        solved_matrix[i] = get_determinant(replace_column(input_matrix, N, i, y_matrix), N) / original_determinant;
        std::cout << (short) std::round(solved_matrix[i]) << std::endl;
    }

    std::cout << std::flush;
    return 0;
}


fat_boi get_determinant(const matrix &input_matrix, const size_t &size) {
    if (size == 1)
        return get_determinant1(input_matrix);
    else if (size == 2)
        return get_determinant2(input_matrix);
    else if (size == 3)
        return get_determinant3(input_matrix);

    if (cache.find(input_matrix) != cache.end())
        return cache[input_matrix];

    fat_boi result = 0;
    fat_boi sign = 1;

    for (size_t i = 0; i < size; i++) {
        result += sign * input_matrix[0][i] * get_determinant(shrink_matrix(
                input_matrix, size, 0, i), size - 1
        );
        sign *= -1;
    }

    cache[input_matrix] = result;
    return result;
}


fat_boi get_determinant1(const matrix &input_matrix) {
    return input_matrix[0][0];
}


fat_boi get_determinant2(const matrix &input_matrix) {
    return input_matrix[0][0] * input_matrix[1][1] - input_matrix[0][1] * input_matrix[1][0];
}


fat_boi get_determinant3(const matrix &input_matrix) {
    return input_matrix[0][0] * (input_matrix[1][1] * input_matrix[2][2] - input_matrix[1][2] * input_matrix[2][1])
        - input_matrix[0][1] * (input_matrix[1][0] * input_matrix[2][2] - input_matrix[1][2] * input_matrix[2][0])
        + input_matrix[0][2] * (input_matrix[1][0] * input_matrix[2][1] - input_matrix[1][1] * input_matrix[2][0]);
}


matrix replace_column(
        matrix input_matrix,
        const size_t &size,
        const size_t &replace_column,
        const std::vector<fat_boi> &replace_values) {

    for (size_t i = 0; i < size; i++) {
        input_matrix[i][replace_column] = replace_values[i];
    }

    return input_matrix;
}


matrix shrink_matrix(
        const matrix &input_matrix,
        const size_t &size,
        const size_t &remove_row,
        const size_t &remove_column) {

    matrix return_matrix(size - 1, std::vector<fat_boi>(size - 1, 0));

    size_t row_marker = 0, column_marker;
    for (size_t row_i = 0; row_i < size; row_i++) {
        if (row_i == remove_row)
            continue;

        column_marker = 0;
        for (size_t col_i = 0; col_i < size; col_i++) {
            if (col_i == remove_column)
                continue;
            return_matrix[row_marker][column_marker] = input_matrix[row_i][col_i];
            column_marker++;
        }
        row_marker++;
    }

    return return_matrix;
}
