# PortfolioManagement-Depleted

Discord bot that allows registered users to fetch data from their Binance account, using their Public and secret API key. 

1 - To register, a user has to type the .register "apikey" "api_secret_key" command

2 - Then the bot will add them to the database and perform a loop every 30 minutes to get the data on his account.

3 - Then the user can use the .pourcentage "30_Min_Iterations" command to see how is balance fluctuated during this time

This was the first version of the code, and the main use of this bot for quite a time. But it was buggy and the loop would crash sometimes so it fell out of use.

Now this bot is still used everyday, but for the .asset command, which allows you to convert value of any registered ticker in Binance to another.
