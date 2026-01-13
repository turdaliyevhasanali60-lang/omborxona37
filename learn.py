from ast import List
class Solution:
    def plusOne(self, digits):
        nums = 0
        for num in digits:
            nums = nums * 10 + num
        nums += 1
        result = []
        while nums > 0:
            result.append(nums % 10)
            nums //= 10
        result.reverse()
        return result

a = Solution()
print(a.plusOne([1,2,3]))