package com.chikie.dao;

import com.chikie.entity.News;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NewsDao {
    @Select("SELECT * FROM news")
    List<News> getAllNews();

    @Select("SELECT * FROM news WHERE id = #{id}")
    News getNewsById(String id);

    @Update("UPDATE news SET title=#{title}, date=#{date}, content=#{content} WHERE id = #{id}")
    int updateNews(@Param("id") String id, @Param("title") String title, @Param("date") String date , @Param("content") String content);

    @Delete("DELETE FROM news WHERE id = #{id}")
    int deleteNews(@Param("id") String id);
}
