import numpy as np

class Queries:
    
    def create_upload_id(mydb,doc_id,patient_id,upload_date,tag):
        mycursor = mydb.cursor()
        sql = "INSERT INTO wound.upload(user_id, patient_id, upload_type,upload_datetime) values(%s,%s,%s,%s)"
        val = (doc_id,patient_id,tag,upload_date)
        mycursor.execute(sql, val)
        mydb.commit()

        sql = "SELECT LAST_INSERT_ID() as id"
        mycursor.execute(sql)
        row = mycursor.fetchone()
        upload_id = row[0]
        mycursor.close()

        return upload_id

    def get_upload_with_filename(mydb,filename):
        mycursor = mydb.cursor()
        sql = "select upload_id from wound.upload_filename where file_name ='"+filename+"'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        upload_ids = []
        for r in result:
            upload_ids.append(r[0])
        mycursor.close()
        return upload_ids

    def insert_into_characterstics_color_model(mydb,TissueDistribution,upload_id):
        mycursor = mydb.cursor()
        for t in TissueDistribution:
            if t['Label'] == 'Eschar' : label = 'eschar'
            elif t['Label'] == 'UnHealthyGranulation' : label = 'UnHealthy_Granulation'
            elif t['Label'] == 'HealthyGranulation' : label = 'Healthy_Granulation'
            elif t['Label'] == 'Slough' : label = 'slough'
            else: label = t['Label']

            if t['area'] < 4: continue;
            sql = "insert into algo_wound_characterstics_details(upload_id,label,area) values("+str(upload_id)+",'"+label+"',"+str(t['area'])+")"
            mycursor.execute(sql)
            mydb.commit()
        mycursor.close()

    def delete_algo_uploads(mydb,upload_ids):
        mycursor = mydb.cursor()
        try:
            len(upload_ids)
        except TypeError:
            upload_ids = [upload_ids]
        NoUploadsDeleted = 0
        for u in upload_ids:
            NoUploadsDeleted = NoUploadsDeleted + 1
            sql = "delete from wound.temperature where upload_id ="+ str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.wound_healing_score where upload_id ="+ str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.upload_filename where upload_id ="+ str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.algo_wound_details where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.algo_peri_wound_details where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.algo_wound_details_before_cleaning where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.algo_peri_wound_details_before_cleaning where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.algo_wound_characterstics_details where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.algo_wound_characterstics_details_before where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            
            sql = "delete from wound.doc_wound_details where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.doc_peri_wound_details where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.doc_wound_details_before_cleaning where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
            sql = "delete from wound.doc_peri_wound_details_before_cleaning where upload_id = "+str(u)
            mycursor.execute(sql)
            mydb.commit()
          
            
            
            sql = "delete from wound.upload where upload_id="+ str(u)
            mycursor.execute(sql)
            mydb.commit()
        mycursor.close()
        return NoUploadsDeleted

    def insert_into_filename(mydb,upload_id,filename):
        mycursor = mydb.cursor()
        sql = "INSERT INTO wound.upload_filename(upload_id, file_name, file_type) values(%s,%s,%s)"
        val = (upload_id,filename,'raw')
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
     

    def insert_begin_end(mydb,wound_image,upload_id,trans_type):
        mycursor = mydb.cursor()
        if trans_type == 'start':
            sql = "delete from wound.model_runtime_update where filename ='" + wound_image+"'"
            mycursor.execute(sql)
            mydb.commit()
            sql = "INSERT INTO wound.model_runtime_update(filename,model_status,upload_id, time_begin) values(%s,%s,%s,CURRENT_TIMESTAMP())"
            val = (wound_image,trans_type,upload_id)
            mycursor.execute(sql, val)
        if trans_type == 'end':
            sql = "UPDATE wound.model_runtime_update SET time_end = CURRENT_TIMESTAMP() where filename = '"+wound_image+"'"
            mycursor.execute(sql)
        mydb.commit()
        mycursor.close()

    def insert_into_wound(mydb,wound_predicted,upload_id,wound_id,image_type):
        cur = mydb.cursor()
        for w in wound_predicted:
            wound_size_width = w['wound_size_width']
            wound_size_height = w['wound_size_height']
            wound_area = w['wound_area']
            wound_conf = w['conf']
            wound_identifier = w['wound_identifier']
            wound_x_center = w['wound_x_center']
            wound_y_center = w['wound_y_center']
            if image_type == "After Cleaning":
                stmt = "INSERT INTO wound.algo_wound_details(upload_id,wound_identifier, wound_area,wound_size_height,wound_size_width,wound_conf,wound_id,wound_x_center,wound_y_center) VALUES ("+str(upload_id)+",'"+wound_identifier+"',"+str(wound_area)+","+str(wound_size_height) +","+str(wound_size_width)+","+str(wound_conf)+","+str(wound_id)+","+str(wound_x_center)+","+str(wound_y_center)+")" 
            else :
                stmt = "INSERT INTO wound.algo_wound_details_before_cleaning(upload_id,wound_identifier, wound_area,wound_size_height,wound_size_width,wound_conf,wound_id,wound_x_center,wound_y_center) VALUES ("+str(upload_id)+",'"+wound_identifier+"',"+str(wound_area)+","+str(wound_size_height) +","+str(wound_size_width)+","+str(wound_conf)+","+str(wound_id)+","+str(wound_x_center)+","+str(wound_y_center)+")" 
            cur.execute(stmt) 
        mydb.commit()
        cur.close()

    def insert_into_periwound(mydb,wound_predicted,upload_id,wound_id,image_type):
        cur = mydb.cursor()
        for w in wound_predicted:
            wound_size_width = w['wound_size_width']
            wound_size_height = w['wound_size_height']
            wound_area = w['wound_area']
            wound_conf = w['conf']
            wound_identifier = w['wound_identifier']
            wound_x_center = w['wound_x_center']
            wound_y_center = w['wound_y_center']
            if image_type == "After Cleaning":
                stmt = "INSERT INTO wound.algo_peri_wound_details(upload_id,wound_identifier, peri_wound_area,peri_wound_size_height,peri_wound_size_width,peri_wound_conf,wound_id,peri_wound_x_center,peri_wound_y_center) VALUES ("+str(upload_id)+",'"+wound_identifier+"',"+str(wound_area)+","+str(wound_size_height) +","+str(wound_size_width)+","+str(wound_conf)+","+str(wound_id)+","+str(wound_x_center)+","+str(wound_y_center)+")" 
            else:
                stmt = "INSERT INTO wound.algo_peri_wound_details_before_cleaning(upload_id,wound_identifier, peri_wound_area,peri_wound_size_height,peri_wound_size_width,peri_wound_conf,wound_id,peri_wound_x_center,peri_wound_y_center) VALUES ("+str(upload_id)+",'"+wound_identifier+"',"+str(wound_area)+","+str(wound_size_height) +","+str(wound_size_width)+","+str(wound_conf)+","+str(wound_id)+","+str(wound_x_center)+","+str(wound_y_center)+")" 
            cur.execute(stmt) 
        mydb.commit()
        cur.close()

    def insert_into_characterstics(mydb,wound_predicted,upload_id,wound_id,image_type):
        cur = mydb.cursor()
        for w in wound_predicted:
            label = w['label']
            wound_size_width = w['wound_size_width']
            wound_size_height = w['wound_size_height']
            wound_area = w['wound_area']
            wound_conf = w['conf']
            wound_identifier = w['wound_identifier']
            wound_x_center = w['wound_x_center']
            wound_y_center = w['wound_y_center']
            if image_type == "After Cleaning":
                stmt = "INSERT INTO wound.algo_wound_characterstics_details(upload_id,wound_identifier, area, size_height,size_width,conf,wound_id,x_center,y_center,label) VALUES  ("+str(upload_id)+",'"+wound_identifier+"',"+str(wound_area)+","+str(wound_size_height) +","+str(wound_size_width)+","+str(wound_conf)+","+str(wound_id)+","+str(wound_x_center)+","+str(wound_y_center)+",'"+label+"')" 
            else:
                stmt = "INSERT INTO wound.algo_wound_characterstics_details_before(upload_id,wound_identifier, area, size_height,size_width,conf,wound_id,x_center,y_center,label) VALUES  ("+str(upload_id)+",'"+wound_identifier+"',"+str(wound_area)+","+str(wound_size_height) +","+str(wound_size_width)+","+str(wound_conf)+","+str(wound_id)+","+str(wound_x_center)+","+str(wound_y_center)+",'"+label+"')"   
            cur.execute(stmt) 
        mydb.commit()
        cur.close()

    def UpdateDepth(mydb,upload_id,filename):
        cur = mydb.cursor()
        depth_output = np.load(filename)
        mindepth = np.amin(depth_output)
        maxdepth = np.amax(depth_output)
        depth = maxdepth - mindepth
        stmt = "update wound.algo_wound_details set wound_size_depth ="+str(depth)+" where upload_id="+str(upload_id) 
        cur.execute(stmt) 
        mydb.commit()
        cur.close()

