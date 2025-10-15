# api/services/feature_builder.py
def build_features(txn_amount, user_avg, user_std, last_10_min_txns):
    features = {}
    features['amount_z'] = (txn_amount - user_avg) / (user_std + 1e-6)
    features['velocity'] = len(last_10_min_txns)
    return features
