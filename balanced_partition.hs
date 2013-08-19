import Data.List
 
--Run Balanced Partition Program
 
main = do
 putStrLn "\nBalanced Partition"
 putStrLn "------------------"
 
 --Insert your list here [1,2,3...]
 --Only works to just over 20 or so as time to run is exponential
 --Your list
 let x = []
 ------------------
 putStrLn ("Solving for -> " ++ show x)
 putStrLn "-------------------"
 
 --Solutions list
 let fsthalf = tail (get_closest $ total_combi x)
 let sndhalf = diff_lists fsthalf x
 let totalfst = sum fsthalf
 let totalsnd = sum sndhalf
 let partition_diff = sum fsthalf - sum sndhalf
 
 --Print solutions
 putStrLn ("First half: " ++ show fsthalf)
 putStrLn ("First half total: " ++ show totalfst)
 putStrLn ("Second half: " ++ show sndhalf)
 putStrLn ("Second half total: " ++ show totalsnd)
 putStrLn ("Minimized Difference: " ++ show partition_diff ++ "\n")
 
--This passes our list of combinations and head list
--To the closest_to_target function
get_closest :: Ord a => [[a]] -> [a]
get_closest [] = []
get_closest (x:[]) = x
get_closest (x:xs) = closest_to_t xs x
 
--Returns the list with the lowest total in the first position
--The closer to 0 = better the balance
closest_to_t :: Ord a => [[a]] -> [a] -> [a]
closest_to_t [] x = x
closest_to_t (y:ys) x
 | head y < head x = closest_to_t ys y
 | otherwise = closest_to_t ys x
 
--Returns the difference of 2 lists
--Used when displaying both balanced lists
diff_lists :: (Num a, Eq a) => [a] -> [a] -> [a]
diff_lists x y = y \\ x
 
--Generate combination of list with totals at front
total_combi :: Integral a => [a] -> [[a]]
total_combi x = sum_to_frt a b
 where b = all_combinations y x
       y = n x
       a = target x
 
--This produces all combinations of list to n
all_combinations :: Int -> [a] -> [[a]]
all_combinations 0 _ = [[]]
all_combinations n y = filter (\x -> length x <= n) (subsequences y)
 
--This adds a (sum of each list) - target ^2
--to the front of each in list
sum_to_frt :: Num a => a -> [[a]] -> [[a]]
sum_to_frt y [] = []
sum_to_frt y (x:xs) = (((sum x)-y)^2 : x) : sum_to_frt y xs
 
--Half number of elements in list
n :: [a] -> Int
n x = (length x `div` 2) + 1
 
--Target value for optimal balance
--Half of total sum of list
target :: (Integral a) => [a] -> a
target x = sum x `div` 2
