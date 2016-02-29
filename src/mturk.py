import boto.mturk.connection
 
sandbox_host = 'mechanicalturk.sandbox.amazonaws.com'
real_host = 'mechanicalturk.amazonaws.com'
 
mturk = boto.mturk.connection.MTurkConnection(
    aws_access_key_id = 'AKIAIQ7G5NLNRHPBJKQQ',
    aws_secret_access_key = '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',
    host = sandbox_host,
    debug = 1 # debug = 2 prints out all requests.
)
 
print boto.Version 
print mturk.get_account_balance() 


url = "https://www.yahoo.com"
title = "A special hit!"
description = "The more verbose description of the job!"
keywords = ["cats", "dogs", "rabbits"]
frame_height = 500 # the height of the iframe holding the external hit
amount = .05
 
questionform = boto.mturk.question.ExternalQuestion( url, frame_height )
 
create_hit_result = mturk.create_hit(
    title = title,
    description = description,
    keywords = keywords,
    question = questionform,
    reward = boto.mturk.price.Price( amount = amount),
    response_groups = ( 'Minimal', 'HITDetail' ), # I don't know what response groups are
)