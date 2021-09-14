import tools as t
import pandas as pd

portfolio_f = "./data/portfolio.json"
profile_f = "./data/profile.json"
transcript_f = "./data/transcript.json"
portfolio_out = "./data/portfolio_clean.csv"
profile_out = "./data/profile_clean.csv"
transcript_out = "./data/transcript_clean.csv"

# Read the files in
portfolio = pd.read_json(portfolio_f, orient='records', lines=True)
profile = pd.read_json(profile_f, orient='records', lines=True)
transcript = pd.read_json(transcript_f, orient='records', lines=True)

# Run cleaning
portfolio = t.clean_portfolio(portfolio)
profile = t.clean_profile(profile)
transcript = t.clean_transcript(transcript)

# Reconciliate ids
portfolio, transcript = t.reconciliate_ids(portfolio, transcript, 'offer_id')
profile, transcript = t.reconciliate_ids(profile, transcript, 'customer_id')

# write the files as csvs
portfolio.to_csv(portfolio_out, index=False)
profile.to_csv(profile_out, index=False)
transcript.to_csv(transcript_out, index=False)
