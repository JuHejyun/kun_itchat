#coding=utf-8
import json

value = "{\\x22username\\x22:\\x229\\x22,\\x22password\\x22:\\x226\\x22,\\x22id\\x22:\\x222c8bfa56-f5d9\\x22, \\x22FName\\x22:\\x22AnkQcAJyrqpg\\x22}"

print(value.encode('utf8').decode('unicode_escape'))

