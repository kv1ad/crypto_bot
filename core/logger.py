def log_rejection(signal_data, reason):
    with open("logs/rejected_signals.log", "a") as f:
        f.write(f"[REJECTED] {signal_data['symbol']} | Reason: {reason}\n")