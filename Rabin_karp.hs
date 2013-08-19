--Rabin Karp String Search
--usage: rabin_karp textbody searchterm
 
import Data.List
import Data.Char
 
--Creates a list of ascii characters to represent a String.
create_ascii_list::String -> [Integer]
create_ascii_list = map (fromIntegral . ord)
 
--Creates a hash of an ascii list.
create_hash :: Num a => [a] -> a
create_hash = sum . zipWith (*) (iterate (* 256) 1) . reverse
 
--Generates a list of substrings of same length as search.
sub_list :: Int -> [a] -> [[a]]
sub_list size [] = []
sub_list size ls@(x:xs)
	| length ls >= size = take size ls : sub_list size xs
 	| otherwise = sub_list size xs
 
--Generate a list of ascii chars from substrings
body_ascii_list :: String -> String -> [[Integer]]
body_ascii_list body search = map create_ascii_list (sub_list (length search) body)
 
--Hash the list of asciis substrings
hash_ascii_list :: String -> String -> [Integer]
hash_ascii_list body search = map create_hash (body_ascii_list body search)
 
--This returns the positions of all matching hashes or error if not found.
return_pos :: Integer -> [Integer] -> [Integer]
return_pos e xs = return_pos' 0 e xs
 
return_pos' i e [] = []
return_pos' i e (x:xs)
	| e == x = i:return_pos' (i + 1) e xs
 	| otherwise = return_pos' (i + 1) e xs
 
{-
 This returns the positions of the searched string in a list
 It takes a body of text and a search term as parameters.
-}
 
rabin_karp :: String -> String -> [Integer]
rabin_karp body search
	| a `elem` b = return_pos a b
	| otherwise = error "Not Found!"
 where
  a = create_hash (create_ascii_list search)
  b = hash_ascii_list body search
