SET 'auto.offset.reset'='earliest';
create stream users_stream with (kafka_topic='users_topic.public.users',value_format='avro');
create stream created_users_stream with (kafka_topic='created_users',value_format='json') as select after->id as user_id, after->username as username,after->email as email, after->hash_password as password, after->is_a_star as star, after->is_admin as is_admin, after->is_email_verified as is_email_verified, after->joined_at as joined_at from users_stream where op in ('c', 'u');


create stream account_stream with (kafka_topic='users_topic.public.account',value_format='avro');

create stream create_account_stream with (kafka_topic='created_account', value_format='json') as select after->user_id as user_id, after->profile_pic as profile_pic, after->is_active as is_active from account_stream where op in ('c','u');


create stream user_to_account as select * from created_users_stream users inner join create_account_stream account within 7 days grace period 30 minutes on users.user_id = account.user_id;

create stream elastic_users_stream_with_key with (kafka_topic='elasticsearch_users_with_key', value_format='json') as
select users_user_id as user_id, CAST(users_user_id as varchar) as user_id_in_string,users_username as username, users_star as star, account_profile_pic as profile_pic, account_is_active as is_active from user_to_account where users_is_email_verified = true;



create stream elasticsearch_users_stream with (kafka_topic='elasticsearch_users', value_format='json') as select * from elastic_users_stream_with_key partition by user_id_in_string;

select * from elasticsearch_users_stream emit changes;
