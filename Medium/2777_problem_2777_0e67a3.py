# 2777. Problem 2777
# LeetCode Link: https://leetcode.com/problems/

from collections import defaultdict

class Solution:
    def countSubarrays(self, nums: list[int], k: int) -> int:
        """
        Counts the number of subarrays where 'k' is the median.

        The problem defines a median for an array 'a' of length 'L' as the
        element at index (L-1)/2 after sorting 'a' (0-indexed).

        This implies two conditions for 'k' to be the median of a subarray:
        1. For odd length subarrays (L = 2P + 1), 'k' is at index P. This means
           there are P elements smaller than 'k' and P elements larger than 'k'.
           So, count_less == count_greater.
        2. For even length subarrays (L = 2P), 'k' is at index P-1. This means
           there are P-1 elements smaller than 'k' and P elements larger than 'k'.
           So, count_less == count_greater - 1.

        We can transform the problem by mapping elements relative to 'k':
        - If num > k, map to 1
        - If num < k, map to -1
        - If num == k, map to 0 (This value for k_idx won't directly be summed)

        Let `balance = count_greater - count_less`. The conditions become:
        - `balance == 0`
        - `balance == 1`

        The approach involves finding the index of 'k' (`k_idx`). Then, we iterate
        outwards from `k_idx`. We use a hash map to store the frequencies of
        balance sums encountered while moving left from `k_idx-1` to `0`.
        Then, we iterate from `k_idx` to `N-1` (rightwards), maintaining a
        `current_sum_right` representing the balance from `k_idx+1` to the
        current element `j`. For each `current_sum_right`, we query the hash map
        for `(-current_sum_right)` and `(1 - current_sum_right)` to find
        matching left segments.

        Args:
            nums: A list of distinct integers.
            k: The integer whose median occurrences we need to count.

        Returns:
            The total number of subarrays where 'k' is the median.
        """
        n = len(nums)
        k_idx = -1

        # 1. Find the index of k and create the transformed array
        # transformed_arr will store 1 for nums[i] > k, -1 for nums[i] < k, and 0 for nums[i] == k
        # The 0 for nums[i] == k is mostly for conceptual completeness; it's skipped in sums.
        transformed_arr = [0] * n
        for i in range(n):
            if nums[i] == k:
                k_idx = i
            elif nums[i] > k:
                transformed_arr[i] = 1
            else: # nums[i] < k
                transformed_arr[i] = -1
        
        # This check is technically not needed due to problem constraints (k is in nums)
        # if k_idx == -1: 
        #     return 0

        ans = 0
        
        # freq_map_left stores the frequency of balance sums encountered
        # when considering segments to the left of k_idx (i.e., from i to k_idx-1).
        # key: balance sum, value: count of segments with that balance sum.
        freq_map_left = defaultdict(int)
        
        # Initialize with 0 balance for the empty segment to the left of k_idx.
        # This covers subarrays starting exactly at k_idx.
        freq_map_left[0] = 1
        
        current_sum_left = 0
        # 2. Populate freq_map_left for elements strictly to the left of k
        # Iterate from k_idx - 1 down to 0
        for i in range(k_idx - 1, -1, -1):
            current_sum_left += transformed_arr[i]
            freq_map_left[current_sum_left] += 1
        
        current_sum_right = 0
        # 3. Iterate from k_idx up to n-1 (elements including k and to its right)
        # For each right endpoint 'j', calculate the balance from k_idx+1 to j.
        # Then, use freq_map_left to find complementing left segments.
        for j in range(k_idx, n):
            # If j is greater than k_idx, it means we are adding elements to the right segment
            if j > k_idx:
                current_sum_right += transformed_arr[j]
            
            # We need current_sum_left + current_sum_right == 0 OR 1
            # So, current_sum_left == -current_sum_right OR current_sum_left == 1 - current_sum_right
            ans += freq_map_left[-current_sum_right]
            ans += freq_map_left[1 - current_sum_right]
            
        return ans

# Solved: 2026-02-15
