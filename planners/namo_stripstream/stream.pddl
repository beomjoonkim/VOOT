(define (stream namo)

  (:stream gen-grasp
    :inputs (?o)
    :domain (and (Pickable ?o))
    :outputs (?grasp ?q_pick ?gconfig)
    :certified (and (Grasp ?grasp)
                    (BaseConf ?q_pick)
                    (GraspConfig ?gconfig)
                    (GraspTransform ?o ?grasp ?q_pick ?gconfig)
                    ))

  (:stream gen-placement
    :inputs (?o ?g ?pick_q ?g_config ?region)
    :domain (and (Pickable ?o)
                 (Grasp ?g)
                 (BaseConf ?pick_q)
                 (GraspTransform ?o ?g ?pick_q ?g_config)
                 (Region ?region)
                 )
    :outputs (?place_q ?obj_pose ?traj)
    :certified (and (BaseConf ?place_q)
                    (Pose ?o ?obj_pose)
                    (PlaceConf ?o ?obj_pose ?place_q)
                    (ObjPoseInRegion ?o ?obj_pose ?place_q ?region)
                    (BTrajWithObject ?o ?g ?pick_q ?place_q ?traj)
                    )
  )

  (:stream gen-base-traj
    :inputs (?q_init ?q_goal)
    :domain (and
                 (BaseConf ?q_init)
                 (BaseConf ?q_goal))
    :outputs (?traj)
    :certified (and (BTraj ?q_init ?q_goal ?traj)))


  (:predicate (TrajPoseCollision ?obstacle ?obstacle_pose ?q_init ?q_goal ?traj)
   (and (BTraj ?q_init ?q_goal ?traj)
        (Pose ?obstacle ?obstacle_pose)
        )
  )

  (:predicate (TrajPoseCollisionWithObject ?holding_o ?grasp ?pick_q ?g_config ?placed_obj ?placed_o_pose ?place_q ?traj)
   (and
         (BTrajWithObject ?holding_o ?grasp ?pick_q ?place_q ?traj)
         (GraspTransform ?holding_o ?grasp ?pick_q ?g_config)
         (Pose ?placed_obj ?placed_o_pose)
         )
  )
)
