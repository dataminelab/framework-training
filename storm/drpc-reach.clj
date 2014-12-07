(def drpc (backtype.storm.LocalDRPC.))
(def cluster (backtype.storm.LocalCluster.))
(def builder (storm.starter.ReachTopology/construct))
(.submitTopology cluster "reach" {} (.createLocalTopology builder drpc))

(.execute drpc "reach" "engineering.twitter.com/blog/5")
(.execute drpc "reach" "tech.backtype.com/blog/123")
(.execute drpc "reach" "not-a-url.com")
