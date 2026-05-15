import hashlib

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def hex_to_binary(hex_str: str) -> str:
    return bin(int(hex_str, 16))[2:].zfill(256)

def count_bit_difference(bin_str1: str, bin_str2: str) -> int:
    diff = 0
    for b1, b2 in zip(bin_str1, bin_str2):
        if b1 != b2:
            diff += 1
    return diff

pangrams = [
    "Чуєш їх, доцю, га? Кумедна ж ти, прощайся без ґольфів!",
    "Жебракують філософи при ґанку церкви в Гадячі, ще й шатро їхнє п'яне знаємо.",
    "Фабрикуймо гідність, лящім їжею, ґав хапаймо, з'єднавці чаш!",
    "Щупак в'ється, ґава дзьобає, фазан їсть хрущів, ціп'як шукає щілину.",
    "Юхиме, в ґудзиках ще захована ця фальшива їжа для щура.",
    "Ця юна ґава хвацько з'їла фініки, щойно приїхавши в Щастя.",
    "Їжак та єнот п'ють чай, ґедзь дзижчить, щука шукає фазана.",
    "Чимчикуй, ґаво, через площі, з'їж цю смачну фісташку й хруща.",
    "Гей, хлопці, не вспію — на ґанку ваша файна їжа знищується бурундучком.",
    "Хвацький юнкор в ґудзиках щулить фейс, п'ючи чай з єгипетських фініків."
]

print(f"{' ':<3} | {'changed bits      ':<13} | {'percent':<10} | {'pangram'}")
print("-" * 80)

for i, base_text in enumerate(pangrams, 1):
    modified_text = base_text[0].swapcase() + base_text[1:]
    
    hash1_hex = sha256(base_text)
    hash2_hex = sha256(modified_text)
    
    bin1 = hex_to_binary(hash1_hex)
    bin2 = hex_to_binary(hash2_hex)
    
    diff_bits = count_bit_difference(bin1, bin2)
    percentage = (diff_bits / 256) * 100
    
    short_base = base_text[:12] + "..."
    short_mod = modified_text[:12] + "..."
    
    print(f"{i:<3} | {diff_bits:<4} out of 256    | {percentage:>5.1f}%    | '{short_base}'")

print("-" * 80)
