
class Equation:

    def __init__(self, file_path='', equation_text=''):
        if file_path:
            with open(file_path, 'r') as f:
                equation_text = f.read()
        if not equation_text:
            raise ValueError('Please pass either a file path or an equation text itself.')
        left_side = equation_text.split('=')[0]
        self.result = int(equation_text.split('=')[1])
        self.digits = left_side.split()

        first_digit = int(self.digits[0])
        # Set coarse bounds to accelerate the process
        self.limits = [(-first_digit, -first_digit)]
        for i in range(1, len(self.digits)):
            prev = self.limits[i - 1]
            curr_num = int(self.digits[i])
            self.limits.append((prev[0] - curr_num, prev[1] + curr_num))

    def _backward_pass(self):
        # Partial sums depending on depth, negating the numbers
        self.partial_results = { len(self.digits): {-self.result} }
        for i in range(len(self.digits) - 1):
            #import ipdb;ipdb.set_trace()
            depth = len(self.digits) - i - 1
            curr_num = int(self.digits[depth])
            prev_results = self.partial_results[depth + 1]
            curr_results = set()
            for res in prev_results:
                res_minus = res - curr_num
                if res_minus >= self.limits[depth - 1][0] and res_minus <= self.limits[depth - 1][1]:
                    curr_results.add(res_minus)
                res_plus = res + curr_num
                if res_plus <= self.limits[depth - 1][1] and res_plus >= self.limits[depth - 1][0]:
                    curr_results.add(res_plus)
            self.partial_results[depth] = curr_results

    def _forward_pass_recursion(self, depth=1, signs=[], curr_sum=None):
        if depth == 1:
            curr_sum = -int(self.digits[0])
        elif depth == len(self.digits):
            eq_str = ''
            for i,sign in enumerate(signs):
                eq_str += f'{self.digits[i]} {sign} '
            eq_str += f'{self.digits[len(self.digits)-1]} = {self.result}'
            self.solutions.append(eq_str)
            return
        curr_digit = int(self.digits[depth])
        next_sums = self.partial_results[depth + 1]
        next_sum_minus = curr_sum - curr_digit
        if next_sum_minus in next_sums:
            # Flipping the sign (cause we were negating the numbers)
            self._forward_pass_recursion(depth + 1, signs + ['+'], next_sum_minus)
        next_sum_plus = curr_sum + curr_digit
        if next_sum_plus in next_sums:
            # Flipping the sign (cause we were negating the numbers)
            self._forward_pass_recursion(depth + 1, signs + ['-'], next_sum_plus)

    def solve(self, verbose=False):
        if (verbose):
            print('Solving...')
        self._backward_pass()
        self.solutions = []
        self._forward_pass_recursion()
        if (verbose):
            print(f'Found {len(self.solutions)} solutions.')

    def print_solutions(self):
        if self.solutions:
            print('Solutions:')
            for solution in self.solutions:
                print(solution)
        else:
            print('No solutions!')


if __name__ == "__main__":
    #eq = Equation(equation_text='7 19 4 3 1 1 1 = 26')
    eq = Equation(file_path="case 2 numbers.txt")
    eq.solve(verbose=True)
    eq.print_solutions()

