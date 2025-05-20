piano_keys = ["A0","a0","B0"]
for i in range (1,8):
    keys = (str(i)+" ").join("CcDdEFfGgAaB ").split()
    piano_keys += keys
piano_keys += ["C8"]

base_freq = 27.5

note_freqs = {piano_keys[i]:base_freq*pow(2,i/12) for i in range(len(piano_keys))}
note_freqs[''] = note_freqs[" "] = 0.0