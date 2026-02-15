# 1251. Problem Title: Average Spending per User
# LeetCode Link: https://leetcode.com/problems/

# Problem Title: Average Spending per User
# Difficulty: Medium
# Category: Hash Table, Array, Sorting

import collections

class Solution:
    def averageSpendingPerUser(self, customers: list[list[int]], orders: list[list[float]]) -> list[list[float]]:
        """
        Calculates the average spending for each user based on their orders.

        The approach involves two main steps:
        1. Aggregate order data: Iterate through all orders and for each customer,
           accumulate their total spending and the count of their orders. A hash map
           (Python dictionary) is used for efficient lookup and storage, mapping
           `customer_id` to a list `[total_cost, order_count]`. Using `collections.defaultdict`
           simplifies the initialization of new customer entries.
        2. Calculate averages and format: Iterate through the aggregated customer data.
           For each customer, calculate `average_spending = total_cost / order_count`.
           The average spending is then rounded to two decimal places.
           Only customers who have placed at least one order will be in our aggregated data,
           naturally satisfying that requirement.
        3. Sort results: The final list of `[customer_id, average_spending]` pairs
           is sorted by `customer_id` in ascending order.

        Args:
            customers: A list of lists, where each inner list is
                       `[customer_id, customer_name]`. This input is actually
                       not strictly needed for the calculation given the problem constraints,
                       as all necessary info comes from `orders`.
            orders: A list of lists, where each inner list is
                    `[order_id, customer_id, order_date, order_cost]`.

        Returns:
            A list of lists, where each inner list contains
            `[customer_id, average_spending]`, sorted by `customer_id`
            in ascending order. `average_spending` is rounded to 2 decimal places.
        """
        # Dictionary to store [total_cost, order_count] for each customer_id
        # Using defaultdict simplifies handling new customer_ids
        customer_spending_data = collections.defaultdict(lambda: [0.0, 0])

        # Step 1: Aggregate order data
        # Iterate through each order to sum up costs and count orders per customer
        for _, customer_id, _, order_cost in orders:
            customer_spending_data[customer_id][0] += order_cost  # Add to total cost
            customer_spending_data[customer_id][1] += 1           # Increment order count

        result = []
        # Step 2: Calculate averages and format
        # Iterate through the aggregated data for each customer
        for customer_id, (total_cost, order_count) in customer_spending_data.items():
            # Customers with no orders would not appear in customer_spending_data,
            # so no explicit check for order_count > 0 is strictly needed here.
            # But it's good practice for robustness in case input guarantees differ.
            # Here, order_count will always be >= 1 for entries in the dict.
            
            average_spending = total_cost / order_count
            # Round to 2 decimal places as per problem statement
            rounded_average_spending = round(average_spending, 2)
            result.append([float(customer_id), rounded_average_spending]) # customer_id might be int, convert to float for consistency with average_spending

        # Step 3: Sort the results by customer_id
        # The key for sorting is the first element of each sublist (customer_id)
        result.sort(key=lambda x: x[0])

        return result

# Time Complexity: O(M + U log U)
# M is the number of orders.
# U is the number of unique customers who placed at least one order.
# O(M) for iterating through the `orders` list to populate the dictionary.
# O(U) for iterating through the `customer_spending_data` dictionary to calculate averages.
# O(U log U) for sorting the `result` list which contains U unique customers.
# In the worst case, U can be up to M (every order from a different customer), so it could be O(M log M).
# In the general case, U <= N (number of customers) and U <= M.
# So, a tighter bound would be O(M + min(N,M) log min(N,M)).

# Space Complexity: O(U)
# O(U) for the `customer_spending_data` dictionary, which stores an entry for each unique customer who placed an order.
# O(U) for the `result` list, which stores the final computed averages for U unique customers.
# Total space is dominated by O(U).

# Solved: 2026-02-15
